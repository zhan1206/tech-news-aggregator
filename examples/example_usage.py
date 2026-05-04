# Tech News Aggregator - 使用示例

本目录包含 Tech News Aggregator 的使用示例。

## 示例 1: 基本使用

```bash
# 运行默认抓取（所有来源）
python scripts/tech_news_aggregator.py
```

## 示例 2: 按来源筛选

```bash
# 只抓取 GitHub Trending
python scripts/tech_news_aggregator.py --sources github_trending

# 抓取 GitHub Trending 和 Hacker News
python scripts/tech_news_aggregator.py --sources github_trending hacker_news
```

## 示例 3: 按技术栈筛选

```bash
# 只看 Python 相关新闻
python scripts/tech_news_aggregator.py --tech-stacks Python

# 同时看 Python、Rust、Go
python scripts/tech_news_aggregator.py --tech-stacks Python Rust Go

# 看前端相关
python scripts/tech_news_aggregator.py --tech-stacks JavaScript TypeScript React Vue
```

## 示例 4: 生成报告

```bash
# 生成 JSON 报告
python scripts/tech_news_aggregator.py --format json --output report.json

# 生成 Markdown 报告
python scripts/tech_news_aggregator.py --format markdown --output report.md

# 生成 HTML 报告
python scripts/tech_news_aggregator.py --format html --output report.html
```

## 示例 5: 组合使用

```bash
# 综合示例：抓取 GitHub Trending 的 Python/Go/Rust 新闻，生成 HTML 报告
python scripts/tech_news_aggregator.py \
  --sources github_trending \
  --tech-stacks Python Go Rust \
  --limit 20 \
  --format html \
  --output tech-trends.html
```

## 示例 6: Python API 使用

```python
#!/usr/bin/env python3
"""
示例：使用 Tech News Aggregator Python API
"""

from scripts.tech_news_aggregator import TechNewsAggregator

def main():
    # 创建聚合器
    aggregator = TechNewsAggregator()
    
    print("正在抓取技术新闻...")
    
    # 抓取新闻
    grouped_news = aggregator.aggregate(
        sources=['github_trending', 'hacker_news', 'dev_to'],
        tech_stacks=['Python', 'Rust', 'Go', 'TypeScript'],
        limit_per_stack=15
    )
    
    # 生成不同格式的报告
    print("\n=== 文本报告 ===")
    print(aggregator.get_trending_summary(grouped_news))
    
    # 保存 JSON 报告
    json_report = aggregator.get_json_report(grouped_news)
    with open('tech-news.json', 'w', encoding='utf-8') as f:
        f.write(json_report)
    print("\nJSON 报告已保存到 tech-news.json")
    
    # 保存 Markdown 报告
    md_report = aggregator.get_markdown_report(grouped_news)
    with open('tech-news.md', 'w', encoding='utf-8') as f:
        f.write(md_report)
    print("Markdown 报告已保存到 tech-news.md")
    
    # 保存 HTML 报告
    html_report = aggregator.get_html_report(grouped_news)
    with open('tech-news.html', 'w', encoding='utf-8') as f:
        f.write(html_report)
    print("HTML 报告已保存到 tech-news.html")

if __name__ == '__main__':
    main()
```

## 示例 7: 自定义技术栈

```python
#!/usr/bin/env python3
"""
示例：添加自定义技术栈并生成报告
"""

from scripts.tech_news_aggregator import (
    TechNewsAggregator, 
    TECH_STACKS, 
    TechStack
)

# 添加新的技术栈
TECH_STACKS['elixir'] = TechStack(
    name='Elixir',
    aliases=['elixir', 'ex'],
    keywords=['elixir', 'phoenix', 'ecto', 'mix'],
    category='language',
    color='\033[96m'
)

TECH_STACKS['haskell'] = TechStack(
    name='Haskell',
    aliases=['haskell', 'hs'],
    keywords=['haskell', 'purescript'],
    category='language',
    color='\033[92m'
)

# 使用自定义技术栈
aggregator = TechNewsAggregator()
grouped_news = aggregator.aggregate(
    sources=['github_trending'],
    tech_stacks=['Python', 'Elixir', 'Haskell'],
    limit_per_stack=10
)

print(aggregator.get_trending_summary(grouped_news))
```

## 示例 8: 定时任务脚本

创建 `daily_report.sh`（Linux/macOS）或 `daily_report.ps1`（Windows）:

### Linux/macOS

```bash
#!/bin/bash
# daily_report.sh - 每日技术新闻报告

DATE=$(date +%Y-%m-%d)
OUTPUT_DIR="reports/${DATE}"

mkdir -p "$OUTPUT_DIR"

echo "生成 ${DATE} 技术新闻报告..."

python scripts/tech_news_aggregator.py \
  --sources github_trending hacker_news dev_to \
  --tech-stacks Python JavaScript TypeScript Rust Go \
  --format html \
  --output "${OUTPUT_DIR}/tech-news.html"

python scripts/tech_news_aggregator.py \
  --sources github_trending hacker_news dev_to \
  --format json \
  --output "${OUTPUT_DIR}/tech-news.json"

echo "报告已生成: ${OUTPUT_DIR}/"
```

### Windows

```powershell
# daily_report.ps1 - 每日技术新闻报告

$Date = Get-Date -Format "yyyy-MM-dd"
$OutputDir = "reports\$Date"

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

Write-Host "生成 ${Date} 技术新闻报告..."

python scripts/tech_news_aggregator.py `
  --sources github_trending hacker_news dev_to `
  --tech-stacks Python JavaScript TypeScript Rust Go `
  --format html `
  --output "${OutputDir}\tech-news.html"

python scripts/tech_news_aggregator.py `
  --sources github_trending hacker_news dev_to `
  --format json `
  --output "${OutputDir}\tech-news.json"

Write-Host "报告已生成: ${OutputDir}"
```

## 示例 9: GitHub Actions 工作流

创建 `.github/workflows/tech-news.yml`:

```yaml
name: Daily Tech News

on:
  schedule:
    # 每天早上 8 点（UTC）运行
    - cron: '0 8 * * *'
  workflow_dispatch:

jobs:
  generate-report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Generate Tech News Report
        run: |
          python scripts/tech_news_aggregator.py \
            --sources github_trending hacker_news dev_to \
            --tech-stacks Python JavaScript TypeScript Rust Go AI/ML \
            --limit 20 \
            --format html \
            --output tech-news-report.html
      
      - name: Generate JSON Data
        run: |
          python scripts/tech_news_aggregator.py \
            --sources github_trending hacker_news dev_to \
            --format json \
            --output tech-news-data.json
      
      - name: Upload Reports
        uses: actions/upload-artifact@v4
        with:
          name: tech-news-reports
          path: |
            tech-news-report.html
            tech-news-data.json
          retention-days: 30
```

## 示例 10: 与 Slack 集成

```python
#!/usr/bin/env python3
"""
示例：生成 Slack 友好的新闻摘要
"""

import json
from scripts.tech_news_aggregator import TechNewsAggregator

def format_slack_message(grouped_news):
    """格式化 Slack 消息"""
    blocks = []
    
    # 标题
    blocks.append({
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "📰 今日技术新闻",
            "emoji": True
        }
    })
    
    # 按技术栈分组
    for stack_name, news_list in sorted(
        grouped_news.items(),
        key=lambda x: len(x[1]),
        reverse=True
    )[:5]:  # 只显示前 5 个技术栈
        if not news_list:
            continue
        
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*🔧 {stack_name}* ({len(news_list)} 条)"
            }
        })
        
        # 显示前 3 条
        for news in news_list[:3]:
            text = f"• <{news.url}|{news.title}>"
            if news.stars:
                text += f" ⭐{news.stars}"
            if news.score:
                text += f" 👍{news.score}"
            
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
                }
            })
    
    return blocks

# 主程序
if __name__ == '__main__':
    aggregator = TechNewsAggregator()
    grouped_news = aggregator.aggregate(
        sources=['github_trending'],
        limit_per_stack=10
    )
    
    blocks = format_slack_message(grouped_news)
    print(json.dumps(blocks, ensure_ascii=False, indent=2))
    
    # 发送 Slack 消息（需要 slack_sdk）
    # from slack_sdk import WebClient
    # client = WebClient(token=os.environ['SLACK_TOKEN'])
    # client.chat_postMessage(channel='#tech-news', blocks=blocks)
```

---

更多示例和用法请参考主 README 文件。
