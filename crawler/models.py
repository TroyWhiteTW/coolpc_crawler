from dataclasses import dataclass
from typing import Dict, Optional, Set

# 網頁上 select name 對應的主要 PC 零組件分類
# Mapping of select element names to main PC component categories
MAIN_CATEGORIES: Dict[str, str] = {
    "n4": "處理器 CPU",
    "n5": "主機板 MB",
    "n6": "記憶體 RAM",
    "n7": "固態硬碟 M.2/SSD",
    "n8": "傳統硬碟 HDD",
    "n10": "散熱器",
    "n11": "水冷",
    "n12": "顯示卡 VGA",
    "n14": "機殼 CASE",
    "n15": "電源供應器 PSU",
}


def get_category_filter(fetch_all: bool) -> Optional[Set[str]]:
    """回傳要抓取的 select name 集合，None 表示全部抓取。
    Return the set of select names to scrape; None means scrape all."""
    if fetch_all:
        return None
    return set(MAIN_CATEGORIES.keys())


@dataclass
class Product:
    category: str
    subcategory: str
    name: str
    price: int
    remark: str  # 例如: 現貨、訂、客訂、限組裝，空字串表示無特殊標記 e.g. "搭機價", "客訂", "限組裝"; empty string if none
