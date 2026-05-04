---
name: tech-news-aggregator
description: AI-powered tech news aggregator that aggregates industry news by technology stack. Automatically fetches from GitHub Trending, Hacker News, Dev.to, and more. Generates comprehensive reports in multiple formats (Text, JSON, Markdown, HTML).
author: Claw Tech
version: 1.0.0
tags: [news, aggregator, tech, github-trending, hacker-news, monitoring]
homepage: https://github.com/zhan1206/tech-news-aggregator
repository: https://github.com/zhan1206/tech-news-aggregator
topics: [news-aggregator, tech-monitoring, developer-tools, automation]
license: MIT
languages:
  - Python
min_python_version: "3.8"
required_permissions:
  - network (for fetching news from APIs)
optional_permissions: []
configurable_options:
  - name: sources
    description: News sources to fetch from
    type: string
    default: "github_trending, hacker_news, dev_to"
  - name: tech_stacks
    description: Technology stacks to filter (empty means all)
    type: string
    default: ""
  - name: limit_per_stack
    description: Maximum news items per tech stack
    type: number
    default: 10
  - name: output_format
    description: Output format (text, json, markdown, html)
    type: string
    default: "text"
---

# Tech News Aggregator

AI-powered tech news aggregator that automatically fetches and categorizes industry news by technology stack. Supports GitHub Trending, Hacker News, Dev.to, and more.

## Features

- **Multi-Source Aggregation**: Fetches news from GitHub Trending, Hacker News, Dev.to, and Reddit
- **Tech Stack Detection**: Automatically identifies and categorizes by 30+ technology stacks
- **Multiple Output Formats**: Supports Text, JSON, Markdown, and HTML reports
- **Flexible Filtering**: Filter by specific sources or technology stacks
- **Rich Metadata**: Captures stars, scores, comments, authors, tags, and more

## Supported Technology Stacks

**Languages**: Python, JavaScript, TypeScript, Rust, Go, Java, C#, C++, Ruby, Swift, Kotlin

**Frameworks**: React, Vue.js, Angular, Svelte, Django, FastAPI, Flask, Spring Boot, Express

**Databases**: PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch

**DevOps**: Docker, Kubernetes, AWS, Azure, GCP, Terraform, Grafana, Prometheus

**AI/ML**: AI/ML, PyTorch, TensorFlow

## Supported Sources

| Source | Weight | Description |
|--------|--------|-------------|
| GitHub Trending | 1.5x | Popular repositories |
| Hacker News | 1.3x | Top tech stories |
| Dev.to | 1.0x | Developer articles |
| Reddit | 1.0x | Programming subreddit |

## Quick Start

```bash
# Install dependencies (only standard library needed)
pip install -r requirements.txt  # Optional, only for development

# Basic usage - fetch all sources
python scripts/tech_news_aggregator.py

# Filter by specific sources
python scripts/tech_news_aggregator.py --sources github_trending hacker_news

# Filter by technology stacks
python scripts/tech_news_aggregator.py --tech-stacks Python JavaScript Rust

# Generate different formats
python scripts/tech_news_aggregator.py --format json --output report.json
python scripts/tech_news_aggregator.py --format markdown --output report.md
python scripts/tech_news_aggregator.py --format html --output report.html

# Combine options
python scripts/tech_news_aggregator.py \
  --sources github_trending \
  --tech-stacks Python Go Rust \
  --limit 20 \
  --format html \
  --output tech-trends.html
```

## Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--sources` | `-s` | News sources to fetch | All sources |
| `--tech-stacks` | `-t` | Tech stacks to filter | All stacks |
| `--limit` | `-l` | Max items per stack | 10 |
| `--github-language` | | GitHub Trending language | None |
| `--format` | `-f` | Output format | text |
| `--output` | `-o` | Output file path | stdout |

## Output Formats

### Text (Default)
Human-readable summary with colored output in terminal.

### JSON
Structured data for programmatic use:
```json
{
  "generated_at": "2026-05-04T11:00:00",
  "total_count": 45,
  "tech_stacks_count": 8,
  "data": {
    "Python": [...],
    "Rust": [...]
  }
}
```

### Markdown
GitHub-flavored markdown report suitable for documentation.

### HTML
Beautiful, responsive web page with styling and interactivity.

## API Usage

```python
from tech_news_aggregator import TechNewsAggregator

# Create aggregator
aggregator = TechNewsAggregator()

# Fetch and aggregate news
grouped_news = aggregator.aggregate(
    sources=['github_trending', 'hacker_news'],
    tech_stacks=['Python', 'Rust', 'Go'],
    limit_per_stack=10
)

# Generate reports in different formats
text_report = aggregator.get_trending_summary(grouped_news)
json_report = aggregator.get_json_report(grouped_news)
markdown_report = aggregator.get_markdown_report(grouped_news)
html_report = aggregator.get_html_report(grouped_news)
```

## Use Cases

1. **Daily Standup**: Get a quick overview of what's trending in your tech stack
2. **Tech Radar**: Build your organization's technology radar
3. **Competitive Intelligence**: Monitor competitor technologies
4. **Market Research**: Analyze technology adoption trends
5. **Content Curation**: Generate tech newsletter content

## GitHub Actions Integration

Add to your workflow (`.github/workflows/news.yml`):

```yaml
name: Tech News Report

on:
  schedule:
    - cron: '0 8 * * *'  # Daily at 8 AM
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

## Extending the Aggregator

### Adding New Sources

```python
class CustomFetcher:
    def __init__(self, http_client):
        self.client = http_client
    
    def fetch(self, **kwargs) -> List[NewsItem]:
        # Fetch and return NewsItem list
        pass

# Register the fetcher
aggregator.fetchers['custom_source'] = CustomFetcher(http_client)
```

### Adding New Tech Stacks

```python
TECH_STACKS['new_stack'] = TechStack(
    name='New Stack',
    aliases=['new', 'ns'],
    keywords=['new-keyword'],
    category='tool',
    color='\033[96m'
)
```

## License

MIT License - feel free to use and modify for your projects.
