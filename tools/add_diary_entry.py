#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="Date to create, in YYYY-MM-DD format")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = Path.cwd()
    date = parse_date(args.date) if args.date else datetime.now(ZoneInfo("Asia/Shanghai"))
    label = f"{date.year}.{date.month}.{date.day}"
    file_name = f"{label}.html"
    blog_path = root / "blogs" / file_name
    list_path = root / "blog-list.html"

    list_html = list_path.read_text(encoding="utf-8")
    entry_line = f'    <a href="blogs/{file_name}" class="item">{label} 日记</a>'

    if f"blogs/{file_name}" not in list_html:
        marker = '    <a href="index.html" class="back">← 返回主页</a>\n\n'
        if marker not in list_html:
            raise RuntimeError("Could not find insertion point in blog-list.html")
        list_html = list_html.replace(marker, f"{marker}{entry_line}\n", 1)

    created = not blog_path.exists()

    if args.dry_run:
        print(f"{'Would create' if created else 'Exists'} {blog_path.relative_to(root)}")
        print("Directory entry ready" if f"blogs/{file_name}" in list_html else "Directory entry missing")
        return

    blog_path.parent.mkdir(parents=True, exist_ok=True)
    if created:
        blog_path.write_text(render_blog(label), encoding="utf-8")
    list_path.write_text(list_html, encoding="utf-8")
    print(f"{'Created' if created else 'No new diary file needed for'} {blog_path.relative_to(root)}")


def parse_date(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d")


def render_blog(label: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <title>日记 {label}</title>
    <style>
        body{{background:#fff;max-width:600px;margin:60px auto;padding:0 20px;font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;}}
        .back{{color:#007AFF;text-decoration:none;margin-bottom:30px;display:inline-block;}}
        .date{{color:#777;margin-bottom:20px;}}
        .text{{font-size:18px;color:#333;line-height:2;white-space: pre-line;}}
    </style>
</head>
<body>
    <a href="../index.html" class="back">← 返回主页</a>
    <div class="date">{label}</div>
    <div class="text">
        今天的问题还没有同步到这里。

        如果今天问了 ChatGPT，我会把问题整理成当天的记录，再更新这一页。
    </div>
</body>
</html>
"""


if __name__ == "__main__":
    main()
