import argparse
import csv
import os
from datetime import datetime

from crawler.models import get_category_filter
from crawler.scraper import fetch_page, parse_products


def crawl(args):
    # 抓取原價屋估價單資料
    print("Fetching CoolPC data...")
    html = fetch_page()
    category_filter = get_category_filter(fetch_all=args.all)
    products = parse_products(html, category_filter)
    print(f"Total products: {len(products)}")

    # 決定輸出路徑
    if args.output:
        output_path = args.output
    else:
        os.makedirs("output", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"output/coolpc_{timestamp}.csv"

    # 寫入 CSV
    scraped_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["category", "subcategory", "name", "price", "remark", "scraped_at"])
        for p in products:
            writer.writerow([p.category, p.subcategory, p.name, p.price, p.remark, scraped_at])

    print(f"Output: {output_path}")


def main():
    # CLI 入口，使用 argparse 子命令
    parser = argparse.ArgumentParser(description="CoolPC product price crawler")
    subparsers = parser.add_subparsers(dest="command")

    # crawl 子命令：抓取商品資料並輸出 CSV
    crawl_parser = subparsers.add_parser("crawl", help="Fetch products and export CSV")
    # --all: 抓取全部 30 個分類（預設只抓主要零組件）
    crawl_parser.add_argument("--all", action="store_true",
                              help="Fetch all 30 categories (default: main components only)")
    # -o: 指定 CSV 輸出路徑
    crawl_parser.add_argument("-o", "--output", help="Output CSV path")

    args = parser.parse_args()
    if args.command == "crawl":
        crawl(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
