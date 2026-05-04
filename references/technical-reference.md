# Tech News Aggregator - 技术参考

本文档包含技术栈新闻聚合器的详细技术说明和扩展指南。

## 📡 数据源 API

### GitHub Search API

**Endpoint**: `GET https://api.github.com/search/repositories`

**参数**:
- `q`: 查询字符串
- `sort`: 排序字段 (stars, forks, updated)
- `order`: 排序顺序 (asc, desc)
- `per_page`: 每页数量 (最大 100)
- `page`: 页码

**示例**:
```bash
# 获取最近一周热门的 Python 项目
curl -s "https://api.github.com/search/repositories?q=language:Python&sort=stars&order=desc&per_page=50" | jq '.items[] | {name, stars, url}'
```

**速率限制**: 未认证 10 次/分钟，认证 30 次/分钟

### Hacker News API

**Base URL**: `https://hacker-news.firebaseio.com/v0`

**Endpoints**:
- `topstories.json`: 获取热门故事 ID 列表
- `newstories.json`: 获取最新故事 ID 列表
- `beststories.json`: 获取最佳故事 ID 列表
- `item/{id}.json`: 获取故事详情

**示例**:
```bash
# 获取前 10 个热门故事
curl -s "https://hacker-news.firebaseio.com/v0/topstories.json" | jq '.[:10]'
```

**无速率限制**，但建议添加适当延迟

### Dev.to API

**Base URL**: `https://dev.to/api`

**Endpoints**:
- `articles`: 获取文章列表
- `articles?tag={tag}`: 按标签筛选
- `articles?username={username}`: 按用户筛选
- `articles/{id}`: 获取文章详情

**参数**:
- `per_page`: 每页数量 (最大 100)
- `page`: 页码

**示例**:
```bash
curl -s "https://dev.to/api/articles?tag=python&per_page=30" | jq '.[].title'
```

**速率限制**: 未公开，建议遵守正常用法

## 🔧 技术栈检测算法

### 关键词匹配

```python
# 伪代码：技术栈检测逻辑
def detect_tech_stack(text):
    text_lower = text.lower()
    for stack_id, stack in TECH_STACKS.items():
        for keyword in stack.keywords:
            if keyword.lower() in text_lower:
                return stack.name
    return None
```

### 关键词优先级

| 优先级 | 关键词类型 | 示例 |
|--------|-----------|------|
| 高 | 完整单词匹配 | `python ` (带空格) |
| 中 | 子串匹配 | `django` |
| 低 | 别名匹配 | `rs` -> `rust` |

### 歧义处理

某些技术栈可能有重叠关键词：
- `React` vs `React Native`
- `Vue` vs `Vue.js` vs `Nuxt`
- `Go` vs `golang`

解决策略：按定义顺序匹配，优先匹配更具体的关键词。

## 📊 报告生成

### 文本格式

使用 ANSI 转义码实现彩色输出：

```python
# 颜色代码
COLORS = {
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'reset': '\033[0m',
}

# 使用
print(f"{COLORS['blue']}标题{COLORS['reset']}")
```

### HTML 模板

HTML 报告使用嵌入式 CSS，无外部依赖：

```html
<style>
  body { font-family: system-ui, sans-serif; }
  .tech-section { border: 1px solid #eee; border-radius: 8px; }
  .news-item { padding: 15px; margin-bottom: 10px; }
</style>
```

### Markdown 格式

使用 GitHub 风格的 Markdown：

- `#` 标题
- `##` 技术栈分组
- `###` 新闻标题
- `|` 表格
- `---` 分隔线
- `` `code` `` 内联代码

## 🔄 GitHub Actions 工作流

### Cron 表达式

```yaml
schedule:
  # 每天早上 8 点
  - cron: '0 8 * * *'
  
  # 每周一早上 9 点
  - cron: '0 9 * * 1'
  
  # 每月第一天早上 10 点
  - cron: '0 10 1 * *'
```

### 工作流触发器

```yaml
on:
  # 定时触发
  schedule:
    - cron: '0 8 * * *'
  
  # 手动触发
  workflow_dispatch:
  
  # 代码推送触发
  push:
    branches: [main]
  
  # PR 触发
  pull_request:
    branches: [main]
```

### 环境变量

```yaml
env:
  PYTHON_VERSION: '3.11'
  TZ: 'Asia/Shanghai'
```

## 🛠 扩展指南

### 添加新来源

```python
from typing import List
from dataclasses import dataclass

@dataclass
class NewsItem:
    title: str
    url: str
    source: str
    source_type: str
    tech_stack: str
    # ... 其他字段

class NewSourceFetcher:
    def __init__(self, http_client):
        self.client = http_client
    
    def fetch(self, **kwargs) -> List[NewsItem]:
        """
        实现新来源的抓取逻辑
        """
        items = []
        
        # 1. 请求 API
        data = self.client.fetch('https://api.example.com/news')
        
        # 2. 解析数据
        for item in json.loads(data):
            # 3. 检测技术栈
            tech_stack = self._detect_tech_stack(item)
            
            # 4. 创建 NewsItem
            news = NewsItem(
                title=item['title'],
                url=item['url'],
                source='New Source',
                source_type='new_source',
                tech_stack=tech_stack,
                # ...
            )
            items.append(news)
        
        return items
    
    def _detect_tech_stack(self, item) -> Optional[str:
        # 技术栈检测逻辑
        pass

# 注册到聚合器
aggregator.fetchers['new_source'] = NewSourceFetcher(http_client)
```

### 添加新输出格式

```python
def get_custom_report(self, grouped_news: Dict[str, List[NewsItem]]) -> str:
    """生成自定义格式报告"""
    lines = []
    
    for stack_name, news_list in grouped_news.items():
        # 自定义格式逻辑
        pass
    
    return '\n'.join(lines)
```

## 📈 性能优化

### 缓存策略

```python
import time
from functools import lru_cache

@lru_cache(maxsize=128)
def fetch_with_cache(url: str, ttl: int = 300):
    """带缓存的 HTTP 请求 (TTL: 秒)"""
    # 实现缓存逻辑
    pass
```

### 并发请求

```python
import concurrent.futures
from threading import Semaphore

# 限制并发数
semaphore = Semaphore(5)

def fetch_with_limit(url):
    with semaphore:
        return http_client.fetch(url)

# 并发执行
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(fetch_with_limit, urls))
```

### 批量处理

```python
# 批量获取 Hacker News 故事
def batch_fetch_stories(story_ids: List[int], batch_size: int = 10):
    batches = [story_ids[i:i+batch_size] 
               for i in range(0, len(story_ids), batch_size)]
    
    all_stories = []
    for batch in batches:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            stories = list(executor.map(fetch_story, batch))
        all_stories.extend(stories)
        time.sleep(0.5)  # 避免过快请求
    
    return all_stories
```

## 🔒 安全考虑

### 输入验证

```python
import re
from urllib.parse import urlparse

def validate_url(url: str) -> bool:
    """验证 URL 安全性"""
    try:
        result = urlparse(url)
        # 只允许 http 和 https
        return result.scheme in ('http', 'https')
    except:
        return False

def sanitize_html(html: str) -> str:
    """清理 HTML 防止 XSS"""
    import html
    return html.escape(html)
```

### 速率限制

```python
import time
from collections import deque

class RateLimiter:
    def __init__(self, max_calls: int, period: int):
        self.max_calls = max_calls
        self.period = period
        self.calls = deque()
    
    def wait(self):
        now = time.time()
        # 清理过期记录
        while self.calls and self.calls[0] < now - self.period:
            self.calls.popleft()
        
        # 检查限制
        if len(self.calls) >= self.max_calls:
            sleep_time = self.calls[0] + self.period - now
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        self.calls.append(time.time())
```

## 📝 日志记录

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# 使用
logger.info("开始抓取新闻...")
logger.warning("API 速率限制接近")
logger.error("抓取失败: %s", error)
```

## 🧪 测试

```python
import unittest
from tech_news_aggregator import TechNewsAggregator

class TestTechNewsAggregator(unittest.TestCase):
    def test_aggregate(self):
        aggregator = TechNewsAggregator()
        result = aggregator.aggregate(
            sources=['github_trending'],
            limit_per_stack=5
        )
        self.assertIsInstance(result, dict)
    
    def test_tech_stack_detection(self):
        # 测试技术栈检测
        pass

if __name__ == '__main__':
    unittest.main()
```
