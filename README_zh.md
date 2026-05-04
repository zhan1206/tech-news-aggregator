# 📰 Tech News Aggregator

AI驱动的技术栈新闻聚合器，自动从 GitHub Trending、Hacker News、Dev.to 等多个来源抓取技术新闻，并按技术栈分类。

[English](README.md) | 中文

## ✨ 功能特点

- **多源聚合**: 支持 GitHub Trending、Hacker News、Dev.to、Reddit 等来源
- **技术栈识别**: 自动识别和分类 30+ 种技术栈
- **多格式输出**: 支持文本、JSON、Markdown、HTML 四种报告格式
- **灵活筛选**: 按来源或技术栈过滤
- **丰富元数据**: 捕获星标数、评分、评论数、作者、标签等信息

## 🔧 支持的技术栈

### 编程语言
Python, JavaScript, TypeScript, Rust, Go, Java, C#, C++, Ruby, Swift, Kotlin

### 前端框架
React, Vue.js, Angular, Svelte

### 后端框架
Django, FastAPI, Flask, Spring Boot, Express

### 数据库
PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch

### DevOps 与云
Docker, Kubernetes, AWS, Azure, GCP, Terraform, Grafana, Prometheus

### AI/ML
AI/ML, PyTorch, TensorFlow

## 📡 支持的来源

| 来源 | 权重 | 描述 |
|------|------|------|
| GitHub Trending | 1.5x | 热门仓库 |
| Hacker News | 1.3x | 热门技术故事 |
| Dev.to | 1.0x | 开发者文章 |
| Reddit | 1.0x | 编程社区 |

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/zanz1206/tech-news-aggregator.git
cd tech-news-aggregator

# 仅需 Python 3.8+，无需额外依赖（纯标准库实现）
```

### 基本使用

```bash
# 抓取所有来源
python scripts/tech_news_aggregator.py

# 按来源筛选
python scripts/tech_news_aggregator.py --sources github_trending hacker_news

# 按技术栈筛选
python scripts/tech_news_aggregator.py --tech-stacks Python JavaScript Rust

# 生成不同格式
python scripts/tech_news_aggregator.py --format json --output report.json
python scripts/tech_news_aggregator.py --format markdown --output report.md
python scripts/tech_news_aggregator.py --format html --output report.html

# 组合使用
python scripts/tech_news_aggregator.py \
  --sources github_trending hacker_news \
  --tech-stacks Python Go Rust \
  --limit 20 \
  --format html \
  --output tech-trends.html
```

## 📖 命令行选项

| 选项 | 简写 | 描述 | 默认值 |
|------|------|------|--------|
| `--sources` | `-s` | 新闻来源 | 所有来源 |
| `--tech-stacks` | `-t` | 技术栈筛选 | 所有栈 |
| `--limit` | `-l` | 每个栈最多显示数 | 10 |
| `--github-language` | | GitHub 语言筛选 | 无 |
| `--format` | `-f` | 输出格式 | text |
| `--output` | `-o` | 输出文件路径 | 标准输出 |

## 📊 输出格式示例

### 文本格式（默认）
```
============================================================
📰 技术栈新闻聚合报告
📅 生成时间: 2026-05-04 11:00:00
============================================================

📊 共抓取 45 条新闻，覆盖 8 个技术栈

------------------------------------------------------------
🔧 Python (12 条)
------------------------------------------------------------

1. awesome-python
   ⭐ 125000 | 👤 vinta | 📝 Python
   📝 A curated list of awesome Python frameworks, libraries...
   🔗 https://github.com/vinta/awesome-python
...
```

### JSON 格式
```json
{
  "generated_at": "2026-05-04T11:00:00",
  "total_count": 45,
  "tech_stacks_count": 8,
  "data": {
    "Python": [
      {
        "title": "awesome-python",
        "url": "https://github.com/vinta/awesome-python",
        "source": "GitHub Trending",
        "tech_stack": "Python",
        "stars": 125000,
        "description": "A curated list of awesome Python frameworks..."
      }
    ]
  }
}
```

### Markdown 格式
生成适合文档使用的 GitHub 风格 Markdown 报告。

### HTML 格式
美观的响应式网页，带有现代样式和交互效果。

## 💻 API 使用

```python
from tech_news_aggregator import TechNewsAggregator

# 创建聚合器
aggregator = TechNewsAggregator()

# 抓取和聚合新闻
grouped_news = aggregator.aggregate(
    sources=['github_trending', 'hacker_news'],
    tech_stacks=['Python', 'Rust', 'Go'],
    limit_per_stack=10
)

# 生成不同格式的报告
text_report = aggregator.get_trending_summary(grouped_news)
json_report = aggregator.get_json_report(grouped_news)
markdown_report = aggregator.get_markdown_report(grouped_news)
html_report = aggregator.get_html_report(grouped_news)
```

## 🎯 使用场景

1. **每日站会**: 快速了解技术栈最新趋势
2. **技术雷达**: 构建组织的技术雷达
3. **竞品分析**: 监控竞品使用的技术
4. **市场研究**: 分析技术采用趋势
5. **内容策展**: 生成技术通讯内容

## 🔄 GitHub Actions 集成

添加到工作流 (`.github/workflows/news.yml`):

```yaml
name: Tech News Report

on:
  schedule:
    - cron: '0 8 * * *'  # 每天早上 8 点
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
            --format html \
            --output tech-news-report.html
      
      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: tech-news-report
          path: tech-news-report.html
```

## 🔧 扩展聚合器

### 添加新的来源

```python
class CustomFetcher:
    def __init__(self, http_client):
        self.client = http_client
    
    def fetch(self, **kwargs) -> List[NewsItem]:
        # 抓取并返回 NewsItem 列表
        pass

# 注册 fetcher
aggregator.fetchers['custom_source'] = CustomFetcher(http_client)
```

### 添加新的技术栈

```python
TECH_STACKS['new_stack'] = TechStack(
    name='New Stack',
    aliases=['new', 'ns'],
    keywords=['new-keyword'],
    category='tool',
    color='\033[96m'
)
```

## 📄 许可证

MIT 许可证 - 可自由使用和修改。
