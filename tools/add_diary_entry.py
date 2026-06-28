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
    entry_block = f'''        <a href="blogs/{file_name}" class="item">
            <span class="date">{label}</span>
            <span>
                <span class="title">{label} 学术记录</span>
                <span class="note">待补充。</span>
            </span>
        </a>'''

    if f"blogs/{file_name}" not in list_html:
        first_item = '        <a href="blogs/'
        index = list_html.find(first_item)
        if index != -1:
            list_html = f"{list_html[:index]}{entry_block}\n{list_html[index:]}"
        else:
            marker = "    </main>"
            if marker not in list_html:
                raise RuntimeError("Could not find insertion point in blog-list.html")
            list_html = list_html.replace(marker, f"{entry_block}\n{marker}", 1)

    created = not blog_path.exists()

    if args.dry_run:
        print(f"{'Would create' if created else 'Exists'} {blog_path.relative_to(root)}")
        print("Academic log entry ready" if f"blogs/{file_name}" in list_html else "Directory entry missing")
        return

    blog_path.parent.mkdir(parents=True, exist_ok=True)
    if created:
        blog_path.write_text(render_blog(label), encoding="utf-8")
    list_path.write_text(list_html, encoding="utf-8")
    print(f"{'Created' if created else 'No new academic log needed for'} {blog_path.relative_to(root)}")


def parse_date(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d")


def render_blog(label: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <title>{label} 学术记录</title>
    <style>
        body{{background:#fbfcf8;max-width:820px;margin:48px auto 82px;padding:0 18px;color:#18211f;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",Arial,sans-serif;}}
        .back{{color:#197b71;text-decoration:none;margin-bottom:36px;display:inline-block;font-weight:700;}}
        .date{{color:#c6742f;font-weight:800;margin-bottom:16px;}}
        .text{{font-size:22px;line-height:2;}}
    </style>
</head>
<body>
    <a href="../blog-list.html" class="back">← 返回学术记录</a>
    <div class="date">{label}</div>
    <div class="text">
        今天还没有写下新的学术记录。
    </div>
</body>
</html>
"""


if __name__ == "__main__":
    main()
