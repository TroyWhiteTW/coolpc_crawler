import re

import requests
from bs4 import BeautifulSoup

def fetch_coolpc_data():
    url = "https://www.coolpc.com.tw/evaluate.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        # 原價屋網頁使用 big5 編碼
        response.encoding = 'big5'
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def parse_coolpc_html(html_content):
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    results = []

    # 原價屋的商品選項在 select 標籤中，通常 name 為 n1, n2, ...
    # 這裡過濾掉重複嵌套的 optgroup
    selects = soup.find_all('select', attrs={'name': re.compile(r'^n\d+')})

    # 原價屋網頁上有 33 個主要的分類標題
    category_titles = [
        "酷幣專區", "品牌主機", "手機/平板/智慧眼鏡", "筆記型電腦", "處理器", "主機板", "記憶體",
        "固態硬碟", "傳統硬碟", "外接硬碟/隨身碟", "散熱器", "顯示卡", "螢幕", "機殼", "電源供應器",
        "機殼風扇", "鍵盤", "滑鼠", "喇叭/耳機", "網路設備", "視訊/音效卡", "線材", "各式轉接頭",
        "擴充卡", "UPS不斷電", "光碟機", "作業系統", "伺服器", "辦公軟體", "電競/工體學椅",
        "遊戲控制器", "直播設備", "儲存裝置"
    ]

    for i, select in enumerate(selects):
        category_main = category_titles[i] if i < len(category_titles) else f"分類{i + 1}"

        # 找出該 select 下的所有 optgroup，但只抓第一層避免重複
        # 或者我們抓所有的 optgroup 並在處理 option 時確保它是該 group 的直接子代
        optgroups = select.find_all('optgroup', recursive=True)

        # 觀察到 HTML 結構中出現了奇怪的 </optgroup> 堆疊，
        # BeautifulSoup 有時會將其解析為嵌套結構。
        # 我們只處理有 label 且包含 option 的 optgroup。

        processed_options = set()

        for group in optgroups:
            category_sub = group.get('label', '')
            if not category_sub:
                continue

            # 只抓直接子代的 option，避免重複計算
            options = group.find_all('option', recursive=False)
            for opt in options:
                # 檢查是否已經處理過（透過物件 id 或位置）
                if opt in processed_options:
                    continue
                processed_options.add(opt)
                # 跳過 disabled 的選項（通常是提示訊息）
                if opt.has_attr('disabled'):
                    continue

                text = opt.text.strip()
                if not text or text.startswith('---'):
                    continue

                # 嘗試解析價格
                # 格式通常是 "商品名稱, $價格 ★" 或 "商品名稱, $價格↘$下殺價 ★"
                price_match = re.search(r'\$(\d+)', text)
                price = int(price_match.group(1)) if price_match else 0

                results.append({
                    "category_main": category_main,
                    "category_sub": category_sub,
                    "name": text,
                    "price": price,
                    "raw_text": text
                })

    return results

def main():
    print("正在爬取原價屋估價單資料...")
    html = fetch_coolpc_data()
    if html:
        items = parse_coolpc_html(html)
        print(f"成功爬取到 {len(items)} 筆商品資料。")

        print("\n範例資料：")
        for item in items:
            print(f"[{item['category_main']}][{item['category_sub']}] {item['name']} -> 價格: {item['price']}")

        # 這裡可以根據需求存成 JSON 或 DataFrame
        # import json
        # with open('coolpc_data.json', 'w', encoding='utf-8') as f:
        #     json.dump(items, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
