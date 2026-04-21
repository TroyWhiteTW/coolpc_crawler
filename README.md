# coolpc-crawler — 原價屋價格爬蟲與歷史比價工具

原價屋（CoolPC）商品價格爬蟲，定期爬取[原價屋線上估價](https://www.coolpc.com.tw/evaluate.php)的電腦零組件價格資料，分類整理後輸出 CSV，並提供歷史價格對比頁面，追蹤漲跌變化。

CoolPC price crawler and historical price comparison tool. Periodically scrapes PC component pricing data from [CoolPC Online Estimator](https://www.coolpc.com.tw/evaluate.php), exports structured CSV files, and provides a web-based price diff viewer to track price changes over time.

### 主要功能 / Features

1. **價格爬取** — 爬取原價屋線上估價的商品價格，依分類整理後輸出 CSV
   **Price Scraping** — Crawl CoolPC product prices by category and export to CSV
2. **歷史價格對比** — 比較不同時間點的價格快照，一目了然查看漲跌與異動（詳見下方對比頁面說明）
   **Historical Price Comparison** — Compare price snapshots across dates to identify changes at a glance (see comparison page section below)

## 技術棧 / Tech Stack

- Python 3.9+（建議搭配 [uv](https://github.com/astral-sh/uv) 管理依賴，亦可直接以原生 Python + pip 執行）
- Python 3.9+ (recommended with [uv](https://github.com/astral-sh/uv) for dependency management; also works with vanilla Python + pip)
- beautifulsoup4（HTML 解析）/ requests（HTTP 請求）
- 目標網頁編碼為 Big5，所有資料在初始 HTML 中，無需 JS 渲染
- Target page is Big5-encoded; all data lives in the initial HTML — no JS rendering required

## 安裝 / Installation

以下以 uv 為例（亦可直接以原生 Python + pip 執行）：
Examples below use uv (also works with vanilla Python + pip):

```bash
uv sync
```

## 使用方式 / Usage

以下以 uv 執行環境為例（若使用 pip，將 `uv run` 替換為直接執行即可）：
Examples below use uv (if using pip, replace `uv run` with `python` directly):

```bash
uv run python main.py crawl            # Only scrape 10 main component categories
uv run python main.py crawl --all      # Scrape all 30 categories
uv run python main.py crawl -o out.csv # Specify output path
```

預設輸出至 `output/coolpc_YYYYMMDD_HHMMSS.csv`。

Output defaults to `output/coolpc_YYYYMMDD_HHMMSS.csv`.

## 分類篩選 / Category Filtering

預設只抓取以下 10 個主要 PC 零組件（定義在 `crawler/models.py` 的 `MAIN_CATEGORIES`）：

By default, only the following 10 main PC component categories are scraped (defined in `MAIN_CATEGORIES` in `crawler/models.py`):

> CPU, Motherboard, RAM, SSD, HDD, CPU Cooler, AIO Liquid Cooler, GPU, PC Case, PSU

使用 `--all` 可抓取全部 30 個分類。

Use `--all` to scrape all 30 categories.

## CSV 欄位 / CSV Fields

`category, subcategory, name, price, remark, scraped_at`

| 欄位 / Field | 說明 / Description |
|---|---|
| `category` | 分類名稱 / Category name |
| `subcategory` | 子分類名稱 / Subcategory name |
| `name` | 商品名稱 / Product name |
| `price` | 價格 (NTD) / Price in NTD |
| `remark` | 備註標記，如「現貨」「訂」「客訂」「限組裝」，多個用 `/` 串接 / Remark tags (e.g. "In Stock", "Pre-order", "Assembly Only"), joined by `/` |
| `scraped_at` | 抓取時間 / Scrape timestamp |

## 專案結構 / Project Structure

```
├── main.py                 # CLI entry point (argparse subcommands)
├── crawler/
│   ├── models.py           # Product dataclass + MAIN_CATEGORIES config
│   └── scraper.py          # fetch_page() + parse_products()
├── output/                 # CSV 輸出目錄 (tracked) / CSV output directory (tracked by Git)
├── docs/                   # GitHub Pages 前端頁面 / Frontend pages for GitHub Pages
│   ├── index.html          # 價格對比主頁面 / Price comparison page
│   ├── style.css
│   ├── app.js
│   └── crawl_history.json  # 爬取歷史清單（自動產生）/ Crawl history list (auto-generated)
├── index.html              # Root redirect → docs/index.html
└── pyproject.toml
```

## 自動排程 / Scheduled Crawling

透過 GitHub Actions 自動定時爬取，無需手動執行。

Automated crawling via GitHub Actions — no manual execution needed.

| 台灣時間 / Taiwan Time | 模式 / Mode | 說明 / Description |
|---|---|---|
| 07:05 / 15:05 / 23:05 | `--all` (ALL) | All 30 categories |
| 11:05 / 19:05 | default (MAIN) | 10 main component categories |

> ⏱ cron 偏移 5 分鐘以錯開整點高峰，減少 GitHub Actions 排程延遲。

> ⏱ Cron offset by 5 minutes to avoid on-the-hour peaks and reduce GitHub Actions scheduling delays.

- commit 訊息格式 / Commit message format: `crawl: 2026-04-18 09:05 ALL`
- 支援從 GitHub Actions 頁面手動觸發，可選 MAIN 或 ALL / Supports manual trigger via `workflow_dispatch` with MAIN/ALL mode selection

## 價格對比頁面 / Price Comparison Page

透過 GitHub Pages 提供靜態價格對比頁面，可選擇兩份爬取快照進行比較。

A static price comparison page is served via GitHub Pages, allowing you to compare two crawl snapshots side by side.

- https://troywhitetw.github.io/coolpc-crawler/docs/index.html
- 支援年月分級選擇、分類摺疊、漲跌標示、MAIN/ALL 模式自動交集比較
- Features: cascading year/month/entry selectors, collapsible categories, price change indicators, automatic MAIN/ALL mode intersection

## 已知問題 / Known Issues

1. 舊價格 (A 側) 預設選擇當月第 6 筆資料，若當月不足 6 筆則選最後一筆，不會自動回推至前一個月
- The old price (A side) defaults to the 6th entry of the current month; if fewer than 6 entries exist, it picks the last one without rolling back to the previous month

## License

MIT
