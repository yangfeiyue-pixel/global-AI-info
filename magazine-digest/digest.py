#!/usr/bin/env python3
"""Daily English magazine digest -> static website (GitHub Pages).

Sources (all legitimate official RSS feeds, free articles only):
  - The New Yorker: https://www.newyorker.com/feed/rss
  - The Economist / The world this week: https://www.economist.com/the-world-this-week/rss.xml

Output: magazine-digest/site/index.html — a mobile-friendly digest page.
Only headlines, summaries and links are published; no paywalled content.
"""

import datetime
import html
import os
import re
import sys

import feedparser

FEEDS = [
    ("The New Yorker", "https://www.newyorker.com/feed/rss", 15),
    ("The Economist · The world this week",
     "https://www.economist.com/the-world-this-week/rss.xml", 15),
]

MAX_SUMMARY_CHARS = 280
SITE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")


def clean(text):
    text = html.unescape(text or "")
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > MAX_SUMMARY_CHARS:
        text = text[:MAX_SUMMARY_CHARS].rstrip() + "…"
    return text


def fetch_feed(name, url, limit):
    print("Fetching %s ..." % name)
    try:
        fp = feedparser.parse(url, request_headers={"User-Agent": "magazine-digest/1.0"})
    except Exception as e:
        print("  failed: %s" % e)
        return []
    items = []
    for e in fp.entries[:limit]:
        items.append({
            "title": clean(getattr(e, "title", "untitled")),
            "link": getattr(e, "link", ""),
            "published": clean(getattr(e, "published", ""))[:32],
            "summary": clean(getattr(e, "summary", getattr(e, "description", ""))),
        })
    print("  got %d items" % len(items))
    return items


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>English Magazine Digest · {date}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: Georgia, 'Times New Roman', serif; background: #faf9f7;
         color: #1a1a1a; line-height: 1.6; padding: 24px 16px 64px; }}
  .wrap {{ max-width: 760px; margin: 0 auto; }}
  header {{ text-align: center; margin-bottom: 36px; padding-bottom: 24px;
            border-bottom: 3px double #1a1a1a; }}
  header h1 {{ font-size: 28px; letter-spacing: 0.02em; }}
  header p {{ color: #6b6b6b; font-size: 14px; margin-top: 8px;
              font-family: -apple-system, sans-serif; }}
  h2 {{ font-size: 20px; margin: 32px 0 16px; padding-bottom: 8px;
        border-bottom: 1px solid #ddd; }}
  article {{ background: #fff; border: 1px solid #e8e6e1; border-radius: 8px;
             padding: 16px 18px; margin-bottom: 14px; }}
  article h3 {{ font-size: 17px; line-height: 1.45; margin-bottom: 6px; }}
  article h3 a {{ color: #1a1a1a; text-decoration: none; }}
  article h3 a:hover {{ text-decoration: underline; }}
  .meta {{ font-size: 12px; color: #999; font-family: -apple-system, sans-serif;
           margin-bottom: 8px; }}
  .sum {{ font-size: 14px; color: #444; font-family: -apple-system, sans-serif; }}
  footer {{ text-align: center; color: #aaa; font-size: 12px; margin-top: 48px;
            font-family: -apple-system, sans-serif; }}
</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>English Magazine Digest</h1>
  <p>{date} · 每日英文杂志免费文章速览 · 标题+摘要+原文链接</p>
</header>
{sections}
<footer>Generated daily by magazine-digest · sources: official RSS feeds</footer>
</div>
</body>
</html>
"""


def build_html(sections, date):
    parts = []
    for name, items in sections:
        parts.append("<h2>%s <span style='color:#999;font-size:14px;'>%d</span></h2>"
                     % (html.escape(name), len(items)))
        if not items:
            parts.append("<p style='color:#999;'>今日暂无更新</p>")
            continue
        for it in items:
            parts.append(
                "<article><h3><a href=\"{link}\" target=\"_blank\" rel=\"noopener\">{title}</a></h3>"
                "<div class=\"meta\">{pub}</div>"
                "<div class=\"sum\">{summary}</div></article>".format(
                    link=html.escape(it["link"], quote=True),
                    title=html.escape(it["title"]),
                    pub=html.escape(it["published"]),
                    summary=html.escape(it["summary"]),
                )
            )
    return PAGE_TEMPLATE.format(date=date, sections="\n".join(parts))


def main():
    sections = [(name, fetch_feed(name, url, limit)) for name, url, limit in FEEDS]
    today = datetime.date.today().isoformat()
    page = build_html(sections, today)
    os.makedirs(SITE_DIR, exist_ok=True)
    out = os.path.join(SITE_DIR, "index.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(page)
    print("Wrote %s (%d bytes)" % (out, len(page.encode("utf-8"))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
