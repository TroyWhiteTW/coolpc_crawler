import re
from typing import List, Optional, Set

import requests
from bs4 import BeautifulSoup, NavigableString

from crawler.models import Product

URL = "https://www.coolpc.com.tw/evaluate.php"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)
PRICE_RE = re.compile(r"\$(\d[\d,]*)")
# 備註標記正面表列，需要新增時在此列表添加即可
# Remark patterns whitelist — add new patterns here as needed
REMARK_PATTERNS = [
    r"~(限組裝)~",
    r"【(限組裝)】",
    r"【(客訂)】",
]
REMARK_RE = re.compile("|".join(REMARK_PATTERNS))
SELECT_NAME_RE = re.compile(r"^n(\d+)$")


def fetch_page() -> str:
    """抓取原價屋估價頁面，回傳 HTML 字串。"""
    resp = requests.get(URL, headers={"User-Agent": USER_AGENT}, timeout=30)
    resp.raise_for_status()
    resp.encoding = "big5hkscs"
    return resp.text


def _get_first_text(tag) -> str:
    """取得 tag 的第一個直接文字節點（跳過子元素）。"""
    for child in tag.children:
        if isinstance(child, NavigableString):
            text = child.strip()
            if text:
                return text
    return ""


def parse_products(
        html: str,
        category_filter: Optional[Set[str]] = None,
) -> List[Product]:
    """解析 HTML，回傳商品列表。

    Args:
        html: 網頁 HTML 字串。
        category_filter: 要保留的 select name 集合 (如 {"n4", "n5"})。
                         None 表示全部保留。
    """
    soup = BeautifulSoup(html, "html.parser")
    products: List[Product] = []

    # 找所有 class=t 的 td，每個對應一個分類
    tds_t = soup.find_all("td", class_="t")

    for td in tds_t:
        # 分類名稱是 td 的第一個文字節點
        category_name = _get_first_text(td)
        if not category_name:
            continue

        # 從 td 的 parent 找 select (因為 HTML 結構破碎，select 可能在同層)
        parent = td.parent
        if not parent:
            continue
        select = parent.find("select", attrs={"name": SELECT_NAME_RE})
        if not select:
            continue

        select_name = select.get("name", "")

        # 過濾分類
        if category_filter is not None and select_name not in category_filter:
            continue

        # 遍歷 optgroup → option
        for optgroup in select.find_all("optgroup"):
            subcategory = optgroup.get("label", "").strip()
            if not subcategory:
                continue

            for opt in optgroup.find_all("option", recursive=False):
                if opt.has_attr("disabled"):
                    continue

                text = opt.get_text(strip=True)
                if not text or text.startswith("---"):
                    continue

                price_match = PRICE_RE.search(text)
                if not price_match:
                    continue

                price = int(price_match.group(1).replace(",", ""))

                # 從價格符號前截取商品名稱 Extract product name before price
                name = PRICE_RE.split(text)[0].rstrip(", ")

                # 備註標記：匹配後從 name 移除，結果 trim
                # Remark tags: extract from name, then strip
                raw_matches = REMARK_RE.findall(name)
                # findall 回傳 tuple（多 group），取非空值去重
                # findall returns tuples (multi-group), pick non-empty, deduplicate
                seen = set()
                remarks = []
                for m in raw_matches:
                    tag = next(g for g in m if g) if isinstance(m, tuple) else m
                    if tag not in seen:
                        seen.add(tag)
                        remarks.append(tag)
                remark = "/".join(remarks)
                name = REMARK_RE.sub("", name).strip()

                products.append(
                    Product(
                        category=category_name,
                        subcategory=subcategory,
                        name=name,
                        price=price,
                        remark=remark,
                    )
                )

    return products
