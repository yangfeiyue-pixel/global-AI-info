# English Magazine Digest

每天早上自动抓取英文杂志官网 RSS 的免费文章，生成一份排版好的速览页面，
通过 GitHub Pages 发布成网站。

**在线地址**：https://yangfeiyue-pixel.github.io/global-AI-info/

## 内容源（均为官网合法 RSS）

- The New Yorker 全站：https://www.newyorker.com/feed/rss
- The Economist · The world this week：https://www.economist.com/the-world-this-week/rss.xml

只收录标题、摘要和原文链接，不复制付费墙后的正文。

## 运行方式

GitHub Actions 每天 23:00 UTC（北京时间次日 07:00）自动跑，
也可以在 Actions 页面点 "Run workflow" 手动触发一次。

## 启用 Pages（只需做一次）

1. 打开仓库 → Settings → Pages
2. Build and deployment → Source 选择 **GitHub Actions**
3. 保存。首次部署成功后，上面的在线地址就能访问了

## 本地预览

```bash
pip install -r magazine-digest/requirements.txt
python magazine-digest/digest.py   # 生成 magazine-digest/site/index.html
open magazine-digest/site/index.html
```
