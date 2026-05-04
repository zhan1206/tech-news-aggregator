#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tech News Aggregator - 按技术栈聚合行业技术新闻
自动从多个来源抓取技术新闻，按技术栈分类，生成聚合报告

Author: Claw Tech
Version: 1.0.0
License: MIT
"""

import json
import re
import sys
import argparse
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode, quote
import html
import textwrap

# ============================================================
# 数据模型
# ============================================================

@dataclass
class NewsItem:
    """新闻条目"""
    title: str
    url: str
    source: str
    source_type: str  # 'github_trending', 'hacker_news', 'reddit', 'twitter', 'dev_to'
    tech_stack: str   # 技术栈标签
    stars: Optional[int] = None
    description: Optional[str] = None
    author: Optional[str] = None
    published_at: Optional[str] = None
    score: Optional[int] = None
    comments: Optional[int] = None
    language: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    summary: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class TechStack:
    """技术栈信息"""
    name: str
    aliases: List[str]  # 别名
    keywords: List[str]  # 关键词
    category: str  # 'language', 'framework', 'tool', 'platform'
    color: str  # 用于输出的颜色代码

# ============================================================
# 技术栈定义
# ============================================================

TECH_STACKS = {
    # 编程语言
    'python': TechStack(
        name='Python',
        aliases=['python', 'py'],
        keywords=['python', 'django', 'flask', 'fastapi', 'pandas', 'numpy', 'pytorch', 'tensorflow', 'jupyter'],
        category='language',
        color='\033[94m'  # 蓝色
    ),
    'javascript': TechStack(
        name='JavaScript',
        aliases=['javascript', 'js', 'node', 'nodejs'],
        keywords=['javascript', 'nodejs', 'node.js', 'npm', 'express', 'react', 'vue', 'angular', 'webpack', 'vite'],
        category='language',
        color='\033[93m'  # 黄色
    ),
    'typescript': TechStack(
        name='TypeScript',
        aliases=['typescript', 'ts'],
        keywords=['typescript', 'ts', 'deno'],
        category='language',
        color='\033[94m'
    ),
    'rust': TechStack(
        name='Rust',
        aliases=['rust', 'rs'],
        keywords=['rust', 'cargo', 'rustlang'],
        category='language',
        color='\033[91m'  # 红色
    ),
    'go': TechStack(
        name='Go',
        aliases=['golang', 'go'],
        keywords=['golang', 'go '],
        category='language',
        color='\033[96m'  # 青色
    ),
    'java': TechStack(
        name='Java',
        aliases=['java', 'jdk', 'jvm'],
        keywords=['java ', 'spring', 'maven', 'gradle', 'jakarta'],
        category='language',
        color='\033[93m'
    ),
    'csharp': TechStack(
        name='C#',
        aliases=['csharp', 'c#', 'dotnet', '.net', 'dotnetcore'],
        keywords=['csharp', 'c#', '.net', 'dotnet', 'asp.net', 'blazor', 'xamarin'],
        category='language',
        color='\033[95m'  # 紫色
    ),
    'cpp': TechStack(
        name='C++',
        aliases=['c++', 'cpp'],
        keywords=['c++', 'cpp', 'stl'],
        category='language',
        color='\033[92m'  # 绿色
    ),
    'ruby': TechStack(
        name='Ruby',
        aliases=['ruby', 'rb'],
        keywords=['ruby', 'rails', 'ruby on rails', 'gem'],
        category='language',
        color='\033[91m'
    ),
    'swift': TechStack(
        name='Swift',
        aliases=['swift', 'ios'],
        keywords=['swift', 'swiftui', 'xcode'],
        category='language',
        color='\033[96m'
    ),
    'kotlin': TechStack(
        name='Kotlin',
        aliases=['kotlin', 'kt'],
        keywords=['kotlin', 'android', 'jetpack'],
        category='language',
        color='\033[96m'
    ),
    
    # 前端框架
    'react': TechStack(
        name='React',
        aliases=['react', 'reactjs'],
        keywords=['react', 'reactjs', 'create-react-app', 'nextjs', 'remix', 'react native'],
        category='framework',
        color='\033[94m'
    ),
    'vue': TechStack(
        name='Vue.js',
        aliases=['vue', 'vuejs', 'nuxt'],
        keywords=['vue', 'vuejs', 'nuxt', 'vuetify', 'nuxtjs'],
        category='framework',
        color='\033[92m'
    ),
    'angular': TechStack(
        name='Angular',
        aliases=['angular', 'ng'],
        keywords=['angular', 'angularjs'],
        category='framework',
        color='\033[91m'
    ),
    'svelte': TechStack(
        name='Svelte',
        aliases=['svelte', 'sveltekit'],
        keywords=['svelte', 'sveltekit', 'svelte.js'],
        category='framework',
        color='\033[93m'
    ),
    
    # 后端框架
    'django': TechStack(
        name='Django',
        aliases=['django', 'drf'],
        keywords=['django', 'djangorestframework', 'drf'],
        category='framework',
        color='\033[92m'
    ),
    'fastapi': TechStack(
        name='FastAPI',
        aliases=['fastapi'],
        keywords=['fastapi'],
        category='framework',
        color='\033[96m'
    ),
    'flask': TechStack(
        name='Flask',
        aliases=['flask'],
        keywords=['flask', 'werkzeug'],
        category='framework',
        color='\033[92m'
    ),
    'spring': TechStack(
        name='Spring',
        aliases=['spring', 'springboot', 'spring boot'],
        keywords=['spring', 'springboot', 'spring boot', 'springcloud'],
        category='framework',
        color='\033[92m'
    ),
    'express': TechStack(
        name='Express',
        aliases=['express', 'expressjs'],
        keywords=['express', 'expressjs'],
        category='framework',
        color='\033[90m'
    ),
    
    # 数据库与存储
    'postgresql': TechStack(
        name='PostgreSQL',
        aliases=['postgresql', 'postgres', 'psql'],
        keywords=['postgresql', 'postgres', 'psql'],
        category='tool',
        color='\033[94m'
    ),
    'mysql': TechStack(
        name='MySQL',
        aliases=['mysql'],
        keywords=['mysql'],
        category='tool',
        color='\033[93m'
    ),
    'mongodb': TechStack(
        name='MongoDB',
        aliases=['mongodb', 'mongo'],
        keywords=['mongodb', 'mongo'],
        category='tool',
        color='\033[92m'
    ),
    'redis': TechStack(
        name='Redis',
        aliases=['redis'],
        keywords=['redis'],
        category='tool',
        color='\033[91m'
    ),
    'elasticsearch': TechStack(
        name='Elasticsearch',
        aliases=['elasticsearch', 'elastic', 'es'],
        keywords=['elasticsearch', 'elastic'],
        category='tool',
        color='\033[96m'
    ),
    
    # DevOps 与云
    'docker': TechStack(
        name='Docker',
        aliases=['docker', 'container'],
        keywords=['docker', 'container', 'containerize'],
        category='tool',
        color='\033[94m'
    ),
    'kubernetes': TechStack(
        name='Kubernetes',
        aliases=['kubernetes', 'k8s', 'k8'],
        keywords=['kubernetes', 'k8s', 'k8'],
        category='tool',
        color='\033[96m'
    ),
    'aws': TechStack(
        name='AWS',
        aliases=['aws', 'amazon web services'],
        keywords=['aws', 'amazon web services', 'amazon aws', 's3', 'ec2', 'lambda'],
        category='platform',
        color='\033[93m'
    ),
    'azure': TechStack(
        name='Azure',
        aliases=['azure', 'microsoft azure'],
        keywords=['azure', 'microsoft azure', 'az'],
        category='platform',
        color='\033[94m'
    ),
    'gcp': TechStack(
        name='GCP',
        aliases=['gcp', 'google cloud', 'google cloud platform'],
        keywords=['gcp', 'google cloud', 'google cloud platform'],
        category='platform',
        color='\033[91m'
    ),
    
    # AI/ML
    'ai': TechStack(
        name='AI/ML',
        aliases=['ai', 'ml', 'machine learning', 'artificial intelligence', 'llm', 'gpt', 'ai模型'],
        keywords=['machine learning', 'artificial intelligence', 'deep learning', 'neural network', 'llm', 'gpt', 'ai模型', '大模型'],
        category='field',
        color='\033[95m'
    ),
    'pytorch': TechStack(
        name='PyTorch',
        aliases=['pytorch', 'torch'],
        keywords=['pytorch', 'torch'],
        category='framework',
        color='\033[91m'
    ),
    'tensorflow': TechStack(
        name='TensorFlow',
        aliases=['tensorflow', 'tf'],
        keywords=['tensorflow', 'keras'],
        category='framework',
        color='\033[93m'
    ),
    
    # 其他工具
    'terraform': TechStack(
        name='Terraform',
        aliases=['terraform', 'tf'],
        keywords=['terraform', 'hashicorp'],
        category='tool',
        color='\033[94m'
    ),
    'grafana': TechStack(
        name='Grafana',
        aliases=['grafana'],
        keywords=['grafana'],
        category='tool',
        color='\033[93m'
    ),
    'prometheus': TechStack(
        name='Prometheus',
        aliases=['prometheus', 'prom'],
        keywords=['prometheus'],
        category='tool',
        color='\033[91m'
    ),
}

# ============================================================
# 新闻来源配置
# ============================================================

NEWS_SOURCES = {
    'github_trending': {
        'name': 'GitHub Trending',
        'base_url': 'https://api.github.com/search/repositories',
        'enabled': True,
        'weight': 1.5,  # 权重因子
    },
    'hacker_news': {
        'name': 'Hacker News',
        'base_url': 'https://hacker-news.firebaseio.com/v0',
        'enabled': True,
        'weight': 1.3,
    },
    'dev_to': {
        'name': 'Dev.to',
        'base_url': 'https://dev.to/api/articles',
        'enabled': True,
        'weight': 1.0,
    },
    'reddit': {
        'name': 'Reddit',
        'base_url': 'https://www.reddit.com/r/programming/hot/.json',
        'enabled': True,
        'weight': 1.0,
    },
}

# ============================================================
# HTTP 客户端
# ============================================================

class HttpClient:
    """简单的 HTTP 客户端"""
    
    DEFAULT_HEADERS = {
        'User-Agent': 'Tech-News-Aggregator/1.0 (Python)',
        'Accept': 'application/json, text/html, application/xml',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
    
    def fetch(self, url: str, headers: Optional[Dict[str, str]] = None) -> Optional[str]:
        """获取 URL 内容"""
        try:
            req = Request(url)
            for key, value in self.DEFAULT_HEADERS.items():
                req.add_header(key, value)
            
            if headers:
                for key, value in headers.items():
                    req.add_header(key, value)
            
            with urlopen(req, timeout=self.timeout) as response:
                return response.read().decode('utf-8')
        except HTTPError as e:
            print(f"HTTP Error {e.code}: {url}", file=sys.stderr)
        except URLError as e:
            print(f"URL Error: {e.reason}", file=sys.stderr)
        except Exception as e:
            print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None

# ============================================================
# 新闻抓取器
# ============================================================

class GitHubTrendingFetcher:
    """GitHub Trending 抓取器"""
    
    def __init__(self, http_client: HttpClient):
        self.client = http_client
    
    def fetch(self, language: Optional[str] = None, since: str = 'daily') -> List[NewsItem]:
        """抓取 GitHub Trending"""
        news_items = []
        
        if language:
            url = f"https://api.github.com/search/repositories?q=created:>{self._get_date(since)}&sort=stars&order=desc&language={language}"
        else:
            url = f"https://api.github.com/search/repositories?q=created:>{self._get_date(since)}&sort=stars&order=desc"
        
        data = self.client.fetch(url)
        if not data:
            return news_items
        
        try:
            result = json.loads(data)
            items = result.get('items', [])[:50]  # 限制数量
            
            for item in items:
                # 检测技术栈
                tech_stack = self._detect_tech_stack(
                    item.get('name', '') + ' ' + item.get('description', '') + ' ' + item.get('topics', [])
                )
                
                if tech_stack:
                    news_items.append(NewsItem(
                        title=item.get('name', ''),
                        url=item.get('html_url', ''),
                        source='GitHub Trending',
                        source_type='github_trending',
                        tech_stack=tech_stack,
                        stars=item.get('stargazers_count'),
                        description=item.get('description'),
                        author=item.get('owner', {}).get('login'),
                        language=item.get('language'),
                        tags=item.get('topics', []),
                        published_at=item.get('created_at', '')[:10],
                    ))
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}", file=sys.stderr)
        
        return news_items
    
    def _get_date(self, since: str) -> str:
        """获取日期范围"""
        days_map = {'daily': 1, 'weekly': 7, 'monthly': 30}
        days = days_map.get(since, 1)
        date = datetime.now() - timedelta(days=days)
        return date.strftime('%Y-%m-%d')
    
    def _detect_tech_stack(self, text: str) -> Optional[str]:
        """检测技术栈"""
        text_lower = text.lower()
        for stack_id, stack in TECH_STACKS.items():
            for keyword in stack.keywords:
                if keyword.lower() in text_lower:
                    return stack.name
        return None


class HackerNewsFetcher:
    """Hacker News 抓取器"""
    
    def __init__(self, http_client: HttpClient):
        self.client = http_client
        self.base_url = 'https://hacker-news.firebaseio.com/v0'
    
    def fetch(self, limit: int = 30) -> List[NewsItem]:
        """抓取 Hacker News"""
        news_items = []
        
        # 获取 top stories
        data = self.client.fetch(f'{self.base_url}/topstories.json')
        if not data:
            return news_items
        
        try:
            story_ids = json.loads(data)[:limit]
            
            for story_id in story_ids:
                story_data = self.client.fetch(f'{self.base_url}/item/{story_id}.json')
                if not story_data:
                    continue
                
                story = json.loads(story_data)
                if story.get('type') != 'story':
                    continue
                
                title = story.get('title', '')
                text = title + ' ' + story.get('text', '')
                tech_stack = self._detect_tech_stack(text)
                
                if tech_stack:
                    news_items.append(NewsItem(
                        title=title,
                        url=story.get('url', f'https://news.ycombinator.com/item?id={story_id}'),
                        source='Hacker News',
                        source_type='hacker_news',
                        tech_stack=tech_stack,
                        score=story.get('score'),
                        comments=story.get('descendants'),
                        author=story.get('by'),
                        published_at=datetime.fromtimestamp(story.get('time', 0)).strftime('%Y-%m-%d') if story.get('time') else None,
                    ))
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}", file=sys.stderr)
        
        return news_items
    
    def _detect_tech_stack(self, text: str) -> Optional[str]:
        """检测技术栈"""
        text_lower = text.lower()
        for stack_id, stack in TECH_STACKS.items():
            for keyword in stack.keywords:
                if keyword.lower() in text_lower:
                    return stack.name
        return None


class DevToFetcher:
    """Dev.to 抓取器"""
    
    def __init__(self, http_client: HttpClient):
        self.client = http_client
    
    def fetch(self, tag: Optional[str] = None, limit: int = 30) -> List[NewsItem]:
        """抓取 Dev.to 文章"""
        news_items = []
        
        if tag:
            url = f'https://dev.to/api/articles?tag={quote(tag)}&per_page={limit}'
        else:
            url = f'https://dev.to/api/articles?per_page={limit}'
        
        data = self.client.fetch(url)
        if not data:
            return news_items
        
        try:
            articles = json.loads(data)
            
            for article in articles:
                title = article.get('title', '')
                text = title + ' ' + article.get('description', '') + ' ' + ' '.join(article.get('tag_list', []))
                tech_stack = self._detect_tech_stack(text)
                
                if tech_stack:
                    news_items.append(NewsItem(
                        title=title,
                        url=article.get('url', ''),
                        source='Dev.to',
                        source_type='dev_to',
                        tech_stack=tech_stack,
                        description=article.get('description'),
                        author=article.get('user', {}).get('name'),
                        published_at=article.get('published_at', '')[:10],
                        tags=article.get('tag_list', []),
                        score=article.get('public_reactions_count'),
                        comments=article.get('comments_count'),
                    ))
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}", file=sys.stderr)
        
        return news_items
    
    def _detect_tech_stack(self, text: str) -> Optional[str]:
        """检测技术栈"""
        text_lower = text.lower()
        for stack_id, stack in TECH_STACKS.items():
            for keyword in stack.keywords:
                if keyword.lower() in text_lower:
                    return stack.name
        return None


# ============================================================
# 新闻聚合器
# ============================================================

class TechNewsAggregator:
    """技术新闻聚合器"""
    
    def __init__(self):
        self.http_client = HttpClient()
        self.fetchers = {
            'github_trending': GitHubTrendingFetcher(self.http_client),
            'hacker_news': HackerNewsFetcher(self.http_client),
            'dev_to': DevToFetcher(self.http_client),
        }
    
    def aggregate(
        self,
        sources: Optional[List[str]] = None,
        tech_stacks: Optional[List[str]] = None,
        limit_per_stack: int = 10,
        github_language: Optional[str] = None,
    ) -> Dict[str, List[NewsItem]]:
        """聚合新闻"""
        if sources is None:
            sources = ['github_trending', 'hacker_news', 'dev_to']
        
        all_news: List[NewsItem] = []
        
        for source_type in sources:
            if source_type not in self.fetchers:
                continue
            
            fetcher = self.fetchers[source_type]
            
            try:
                if source_type == 'github_trending':
                    news = fetcher.fetch(language=github_language)
                elif source_type == 'hacker_news':
                    news = fetcher.fetch(limit=50)
                elif source_type == 'dev_to':
                    news = fetcher.fetch(limit=30)
                else:
                    news = []
                
                all_news.extend(news)
            except Exception as e:
                print(f"Error fetching {source_type}: {e}", file=sys.stderr)
        
        # 按技术栈分组
        grouped: Dict[str, List[NewsItem]] = {}
        
        for news in all_news:
            if tech_stacks and news.tech_stack not in tech_stacks:
                continue
            
            if news.tech_stack not in grouped:
                grouped[news.tech_stack] = []
            
            if len(grouped[news.tech_stack]) < limit_per_stack:
                grouped[news.tech_stack].append(news)
        
        return grouped
    
    def get_trending_summary(self, grouped_news: Dict[str, List[NewsItem]]) -> str:
        """生成趋势摘要"""
        lines = []
        lines.append("=" * 60)
        lines.append("📰 技术栈新闻聚合报告")
        lines.append(f"📅 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 60)
        lines.append("")
        
        # 按新闻数量排序
        sorted_stacks = sorted(
            grouped_news.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
        
        total_count = sum(len(news) for _, news in sorted_stacks)
        lines.append(f"📊 共抓取 {total_count} 条新闻，覆盖 {len(sorted_stacks)} 个技术栈")
        lines.append("")
        
        for stack_name, news_list in sorted_stacks:
            if not news_list:
                continue
            
            lines.append("-" * 60)
            lines.append(f"🔧 {stack_name} ({len(news_list)} 条)")
            lines.append("-" * 60)
            
            for i, news in enumerate(news_list, 1):
                lines.append(f"\n{i}. {news.title}")
                
                # 显示额外信息
                meta_parts = []
                if news.stars:
                    meta_parts.append(f"⭐ {news.stars}")
                if news.score:
                    meta_parts.append(f"👍 {news.score}")
                if news.comments:
                    meta_parts.append(f"💬 {news.comments}")
                if news.author:
                    meta_parts.append(f"👤 {news.author}")
                if news.language:
                    meta_parts.append(f"📝 {news.language}")
                
                if meta_parts:
                    lines.append(f"   {' | '.join(meta_parts)}")
                
                if news.description:
                    desc = textwrap.shorten(news.description, width=80, placeholder="...")
                    lines.append(f"   📝 {desc}")
                
                lines.append(f"   🔗 {news.url}")
            
            lines.append("")
        
        lines.append("=" * 60)
        lines.append("报告结束")
        lines.append("=" * 60)
        
        return '\n'.join(lines)
    
    def get_json_report(self, grouped_news: Dict[str, List[NewsItem]]) -> str:
        """生成 JSON 报告"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_count': sum(len(news) for _, news in grouped_news.items()),
            'tech_stacks_count': len(grouped_news),
            'data': {
                stack_name: [news.to_dict() for news in news_list]
                for stack_name, news_list in grouped_news.items()
            }
        }
        return json.dumps(report, ensure_ascii=False, indent=2)
    
    def get_markdown_report(self, grouped_news: Dict[str, List[NewsItem]]) -> str:
        """生成 Markdown 报告"""
        lines = []
        lines.append("# 📰 技术栈新闻聚合报告")
        lines.append("")
        lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        # 按新闻数量排序
        sorted_stacks = sorted(
            grouped_news.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
        
        total_count = sum(len(news) for _, news in sorted_stacks)
        lines.append(f"**统计**: 共 {total_count} 条新闻，覆盖 {len(sorted_stacks)} 个技术栈")
        lines.append("")
        
        for stack_name, news_list in sorted_stacks:
            if not news_list:
                continue
            
            # 技术栈标题
            stack_id = stack_name.lower().replace('#', '').replace('/', '-').replace(' ', '-')
            lines.append(f"## 🔧 {stack_name}")
            lines.append("")
            
            for i, news in enumerate(news_list, 1):
                lines.append(f"### {i}. {news.title}")
                lines.append("")
                
                if news.description:
                    lines.append(f"{news.description}")
                    lines.append("")
                
                # 元信息表格
                lines.append("| 属性 | 值 |")
                lines.append("|------|-----|")
                if news.stars:
                    lines.append(f"| ⭐ Stars | {news.stars} |")
                if news.score:
                    lines.append(f"| 👍 Score | {news.score} |")
                if news.comments:
                    lines.append(f"| 💬 Comments | {news.comments} |")
                if news.author:
                    lines.append(f"| 👤 Author | {news.author} |")
                if news.language:
                    lines.append(f"| 📝 Language | {news.language} |")
                if news.published_at:
                    lines.append(f"| 📅 Published | {news.published_at} |")
                lines.append(f"| 🔗 Link | [View on {news.source}]({news.url}) |")
                lines.append("")
                
                if news.tags:
                    lines.append(f"**Tags**: {' '.join(f'`{tag}`' for tag in news.tags[:5])}")
                    lines.append("")
                
                lines.append("---")
                lines.append("")
        
        lines.append("*报告由 Tech News Aggregator 自动生成*")
        
        return '\n'.join(lines)
    
    def get_html_report(self, grouped_news: Dict[str, List[NewsItem]]) -> str:
        """生成 HTML 报告"""
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>技术栈新闻聚合报告</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; border-radius: 12px; margin-bottom: 30px; }}
        h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .meta {{ opacity: 0.9; font-size: 1.1em; }}
        .stats {{ background: white; padding: 20px; border-radius: 8px; margin-bottom: 30px; display: flex; gap: 30px; }}
        .stat {{ text-align: center; }}
        .stat-value {{ font-size: 2em; font-weight: bold; color: #667eea; }}
        .stat-label {{ color: #666; }}
        .tech-section {{ background: white; border-radius: 12px; padding: 25px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .tech-header {{ display: flex; align-items: center; gap: 15px; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 2px solid #eee; }}
        .tech-icon {{ width: 50px; height: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.5em; color: white; }}
        .tech-name {{ font-size: 1.5em; font-weight: 600; }}
        .tech-count {{ background: #667eea; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.9em; }}
        .news-item {{ padding: 20px; border: 1px solid #eee; border-radius: 8px; margin-bottom: 15px; transition: all 0.3s; }}
        .news-item:hover {{ border-color: #667eea; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15); }}
        .news-title {{ font-size: 1.2em; font-weight: 600; color: #333; margin-bottom: 10px; }}
        .news-title a {{ color: inherit; text-decoration: none; }}
        .news-title a:hover {{ color: #667eea; }}
        .news-meta {{ display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 10px; font-size: 0.9em; color: #666; }}
        .news-meta span {{ display: flex; align-items: center; gap: 5px; }}
        .news-desc {{ color: #555; margin-bottom: 15px; }}
        .news-tags {{ display: flex; gap: 8px; flex-wrap: wrap; }}
        .tag {{ background: #f0f0f0; padding: 4px 12px; border-radius: 20px; font-size: 0.85em; color: #666; }}
        footer {{ text-align: center; padding: 30px; color: #999; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📰 技术栈新闻聚合报告</h1>
            <p class="meta">📅 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </header>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-value">{sum(len(news) for _, news in grouped_news.items())}</div>
                <div class="stat-label">总新闻数</div>
            </div>
            <div class="stat">
                <div class="stat-value">{len(grouped_news)}</div>
                <div class="stat-label">技术栈数</div>
            </div>
            <div class="stat">
                <div class="stat-value">{len([n for _, news in grouped_news.items() for n in news if n.source_type == 'github_trending'])}</div>
                <div class="stat-label">GitHub Trending</div>
            </div>
            <div class="stat">
                <div class="stat-value">{len([n for _, news in grouped_news.items() for n in news if n.source_type == 'hacker_news'])}</div>
                <div class="stat-label">Hacker News</div>
            </div>
        </div>
"""

        # 按新闻数量排序
        sorted_stacks = sorted(
            grouped_news.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
        
        for stack_name, news_list in sorted_stacks:
            if not news_list:
                continue
            
            html_content += f"""
        <div class="tech-section">
            <div class="tech-header">
                <div class="tech-icon">🔧</div>
                <div class="tech-name">{stack_name}</div>
                <div class="tech-count">{len(news_list)} 条</div>
            </div>
"""
            
            for news in news_list:
                meta_items = []
                if news.stars:
                    meta_items.append(f'<span>⭐ {news.stars}</span>')
                if news.score:
                    meta_items.append(f'<span>👍 {news.score}</span>')
                if news.comments:
                    meta_items.append(f'<span>💬 {news.comments}</span>')
                if news.author:
                    meta_items.append(f'<span>👤 {news.author}</span>')
                if news.language:
                    meta_items.append(f'<span>📝 {news.language}</span>')
                
                tags_html = ''.join(f'<span class="tag">{tag}</span>' for tag in news.tags[:5])
                
                html_content += f"""
            <div class="news-item">
                <div class="news-title">
                    <a href="{news.url}" target="_blank">{html.escape(news.title)}</a>
                </div>
                <div class="news-meta">{" ".join(meta_items)}</div>
"""
                
                if news.description:
                    html_content += f"""
                <div class="news-desc">{html.escape(news.description)}</div>
"""
                
                if tags_html:
                    html_content += f"""
                <div class="news-tags">{tags_html}</div>
"""
                
                html_content += """
            </div>
"""
            
            html_content += """
        </div>
"""
        
        html_content += """
        <footer>
            <p>📊 由 Tech News Aggregator 自动生成</p>
        </footer>
    </div>
</body>
</html>"""
        
        return html_content


# ============================================================
# 主程序
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description='Tech News Aggregator - 按技术栈聚合行业技术新闻',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 抓取所有来源
  python tech_news_aggregator.py
  
  # 只抓取 GitHub Trending
  python tech_news_aggregator.py --sources github_trending
  
  # 指定技术栈
  python tech_news_aggregator.py --tech-stacks Python JavaScript Rust
  
  # 生成 JSON 报告
  python tech_news_aggregator.py --format json --output report.json
  
  # 生成 Markdown 报告
  python tech_news_aggregator.py --format markdown --output report.md
  
  # 生成 HTML 报告
  python tech_news_aggregator.py --format html --output report.html
        """
    )
    
    parser.add_argument(
        '--sources', '-s',
        nargs='+',
        choices=['github_trending', 'hacker_news', 'dev_to', 'reddit'],
        default=['github_trending', 'hacker_news', 'dev_to'],
        help='指定新闻来源 (默认: github_trending hacker_news dev_to)'
    )
    
    parser.add_argument(
        '--tech-stacks', '-t',
        nargs='+',
        help='指定技术栈 (默认: 所有)'
    )
    
    parser.add_argument(
        '--limit', '-l',
        type=int,
        default=10,
        help='每个技术栈最多显示数量 (默认: 10)'
    )
    
    parser.add_argument(
        '--github-language',
        help='GitHub Trending 语言筛选 (如: python, javascript, go)'
    )
    
    parser.add_argument(
        '--format', '-f',
        choices=['text', 'json', 'markdown', 'html'],
        default='text',
        help='输出格式 (默认: text)'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='输出文件路径 (默认: 标准输出)'
    )
    
    parser.add_argument(
        '--color',
        action='store_true',
        default=sys.stdout.isatty(),
        help='使用彩色输出 (默认: 自动检测)'
    )
    
    args = parser.parse_args()
    
    # 创建聚合器
    aggregator = TechNewsAggregator()
    
    print("🔍 正在抓取新闻...", file=sys.stderr)
    
    # 聚合新闻
    grouped_news = aggregator.aggregate(
        sources=args.sources,
        tech_stacks=args.tech_stacks,
        limit_per_stack=args.limit,
        github_language=args.github_language,
    )
    
    # 生成报告
    if args.format == 'json':
        report = aggregator.get_json_report(grouped_news)
    elif args.format == 'markdown':
        report = aggregator.get_markdown_report(grouped_news)
    elif args.format == 'html':
        report = aggregator.get_html_report(grouped_news)
    else:
        report = aggregator.get_trending_summary(grouped_news)
    
    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✅ 报告已保存到: {args.output}", file=sys.stderr)
    else:
        print(report)


if __name__ == '__main__':
    main()
