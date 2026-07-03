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
    iso_label = date.strftime("%Y-%m-%d")
    file_name = f"{label}.html"
    blog_path = root / "blogs" / file_name
    list_path = root / "blog-list.html"

    list_html = list_path.read_text(encoding="utf-8")
    entry_block = f'''                <a class="post-item" href="blogs/{file_name}">
                    <h3 class="post-title">{label} 学术记录</h3>
                    <p class="post-summary">今天还没有写下新的学术记录。</p>
                    <div class="post-meta">
                        <span>zhangyuxuan</span>
                        <span>{iso_label}</span>
                        <span>阅读:0</span>
                        <span>评论:0</span>
                        <span>推荐:0</span>
                    </div>
                </a>'''

    if f"blogs/{file_name}" not in list_html:
        first_item = '                <a class="post-item" href="blogs/'
        index = list_html.find(first_item)
        if index != -1:
            list_html = f"{list_html[:index]}{entry_block}\n{list_html[index:]}"
        else:
            marker = "            </section>"
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
        blog_path.write_text(render_blog(label, iso_label, file_name, date.year, date.month), encoding="utf-8")
    list_path.write_text(list_html, encoding="utf-8")
    print(f"{'Created' if created else 'No new academic log needed for'} {blog_path.relative_to(root)}")


def parse_date(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d")


def render_blog(label: str, iso_label: str, file_name: str, year: int, month: int) -> str:
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <title>{label} 学术记录</title>
    <link rel="stylesheet" href="../assets/site.css">
</head>
<body>
    <div class="topbar">
        <div class="topbar-inner">
            <span>zhangyuxuan.xin</span>
            <div class="topbar-links">
                <a href="../index.html">所有记录</a>
                <a href="../blog-list.html">学术目录</a>
                <a href="{file_name}">最新一篇</a>
            </div>
        </div>
    </div>

    <header class="site-header">
        <h1 class="site-title"><a href="../index.html">zhangyuxuan</a></h1>
        <nav class="site-nav">
            <a href="../index.html">首页</a>
            <a href="../blog-list.html">标签</a>
            <a href="../blog-list.html">随笔</a>
            <a href="{file_name}">新随笔</a>
            <a href="mailto:contact@zhangyuxuan.xin">联系</a>
            <a href="../blog-list.html">管理</a>
        </nav>
        <div class="site-stats">
            <span>随笔 - 1</span>
            <span>文章 - 0</span>
            <span>评论 - 0</span>
            <span>阅读 - 0</span>
        </div>
    </header>

    <div class="site-grid">
        <aside class="sidebar">
            <section class="profile-card">
                <div class="profile-name">zhangyuxuan</div>
                <div class="profile-stats">
                    <div><strong>2026.6</strong><span>建站</span></div>
                    <div><strong>1</strong><span>随笔</span></div>
                    <div><strong>2</strong><span>方向</span></div>
                </div>
                <a class="follow" href="../blog-list.html">+ 关注学术记录</a>
            </section>

            <section class="side-section">
                <h2 class="side-title">随笔档案</h2>
                <ul class="side-list">
                    <li><a href="{file_name}">{year}年{month}月(1)</a></li>
                </ul>
            </section>
        </aside>

        <main class="content article">
            <div class="article-date">{label}</div>
            <h1>{label} 学术记录</h1>
            <p>今天还没有写下新的学术记录。</p>
            <div class="post-meta">
                <span>zhangyuxuan</span>
                <span>{iso_label}</span>
                <span>阅读:0</span>
                <span>评论:0</span>
                <span>推荐:0</span>
            </div>
            <a class="back-link" href="../blog-list.html">返回学术记录</a>
        </main>
    </div>

    <footer class="site-footer">zhangyuxuan.xin · academic notes since 2026.6.29</footer>
</body>
</html>
"""


if __name__ == "__main__":
    main()
