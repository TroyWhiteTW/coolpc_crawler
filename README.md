# coolpc-crawler

爬取[原價屋線上估價](https://www.coolpc.com.tw/evaluate.php)的商品價格資料，分類整理後輸出 CSV。

Scrapes product pricing data from [CoolPC Online Estimator](https://www.coolpc.com.tw/evaluate.php) and exports it as a structured CSV.

## 技術棧 / Tech Stack

- Python 3.9 + [uv](https://github.com/astral-sh/uv)
- beautifulsoup4 (HTML parsing) / requests (HTTP)
- 目標網頁編碼為 Big5，所有資料在初始 HTML 中（無需 JS 渲染）
- Target page is Big5-encoded; all data is in the initial HTML (no JS rendering required)

## 安裝 / Installation

```bash
uv sync
```

## 使用方式 / Usage

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
└── pyproject.toml
```

## 自動排程 / Scheduled Crawling

透過 GitHub Actions 自動定時爬取，無需手動執行。

Automated crawling via GitHub Actions — no manual execution needed.

| 台灣時間 / Taiwan Time | 模式 / Mode | 說明 / Description |
|---|---|---|
| 09:00 / 15:00 / 21:00 | `--all` (ALL) | All 30 categories |
| 12:00 / 18:00 | default (MAIN) | 10 main component categories |

- commit 訊息格式 / Commit message format: `crawl: 2026-04-18 09:00 ALL`
- 支援從 GitHub Actions 頁面手動觸發，可選 MAIN 或 ALL / Supports manual trigger via `workflow_dispatch` with MAIN/ALL mode selection

## License

MIT
