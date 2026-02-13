# AI趋势新闻收集使徒

一个专注于AI商业价值和研发提效的自动化新闻收集系统。

## 📋 系统概述

本系统通过RSS订阅、智能筛选和自动化工作流，为您持续提供高质量的AI趋势新闻，重点关注：
- **商业应用价值**：可量化的ROI、成本节约、效率提升案例
- **研发提效工具**：开发框架、自动化工具、最佳实践
- **行业前沿动态**：技术突破、市场趋势、政策变化

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <your-repo-url>
cd ai-news-collector

# 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装依赖
pip install feedparser requests jinja2 pyyaml
```

### 2. 配置设置

编辑 `config.yaml` 文件：

```yaml
# 基本配置
output_dir: './output'
min_score_threshold: 3.5

# 通知渠道（可选）
notification_channels:
  - file
  - telegram  # 需要填写telegram.bot_token和telegram.chat_id
```

### 3. 运行系统

```bash
# 手动运行一次
python automation_workflow.py

# 查看输出
ls output/
cat output/daily_summary_*.md
```

## 📅 自动化部署

### 使用cron（Linux/Mac）

```bash
# 编辑crontab
crontab -e

# 添加以下行（每天9点运行）
0 9 * * * cd /path/to/ai-news-collector && /usr/bin/python3 automation_workflow.py >> /var/log/ai-news.log 2>&1

# 每小时检查RSS更新
0 * * * * cd /path/to/ai-news-collector && /usr/bin/python3 automation_workflow.py --check-only >> /var/log/ai-news-check.log 2>&1
```

### 使用Windows任务计划程序

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器为"每天" 9:00
4. 操作选择"启动程序"
5. 程序: `python.exe`
6. 参数: `automation_workflow.py`
7. 起始于: `C:\path\to\ai-news-collector`

### 使用Docker（可选）

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "automation_workflow.py"]
```

## 🔧 配置文件说明

### 主要配置文件

| 文件 | 说明 |
|------|------|
| `config.yaml` | 系统运行参数和通知设置 |
| `rss_sources.md` | RSS源列表（可编辑） |
| `news_filter_criteria.md` | 新闻筛选标准 |
| `content_template.md` | 输出内容模板 |

### 自定义RSS源

编辑 `rss_sources.md` 文件，按照表格格式添加新的RSS源：

```markdown
| 来源名称 | RSS URL | 主要分类 | 优先级 | 语言 |
|----------|---------|----------|--------|------|
| TechCrunch AI | https://techcrunch.com/category/artificial-intelligence/feed/ | 商业应用 | 5 | en |
```

### 调整筛选标准

修改 `news_filter_criteria.md` 中的关键词和评分规则，以适应您的具体需求。

## 📊 输出格式

系统生成以下类型的输出文件：

### 每日简报 (`daily_summary_YYYY-MM-DD.md`)
- 今日亮点文章
- 商业应用分类
- 研发提效工具
- 行业动态汇总

### 详细文章列表 (`detailed_articles_YYYY-MM-DD.json`)
- 包含所有筛选后文章的完整信息
- 评分详情和分类标签
- 适合进一步处理或集成

### 周度/月度报告
- 趋势分析和预测
- 最佳案例评选
- 完整文章清单

## 🛠️ 扩展功能

### 添加新的通知渠道

在 `automation_workflow.py` 中添加新的通知方法：

```python
def send_to_slack(self, content: str):
    """发送到Slack"""
    # 实现Slack通知逻辑
    pass
```

然后在 `config.yaml` 的 `notification_channels` 中添加 `slack`。

### 自定义评分算法

修改 `calculate_article_score` 方法中的各个评估函数，调整权重或添加新的评估维度。

### 多语言支持

系统支持多语言内容处理，在 `config.yaml` 中配置 `primary_language` 和 `secondary_languages`。

## 📈 维护和监控

### 日志查看

```bash
# 查看最近的日志
tail -f /var/log/ai-news.log

# 检查错误
grep "ERROR" /var/log/ai-news.log
```

### 性能优化

- 启用缓存：`enable_cache: true`
- 调整请求超时：`request_timeout: 30`
- 设置重试次数：`max_retries: 3`

### 数据备份

定期备份 `output/` 目录以保存历史数据：

```bash
# 每周备份
tar -czf ai-news-backup-$(date +%Y-%W).tar.gz output/
```

## 🤝 贡献和改进

欢迎提交Issue和Pull Request：

1. **添加新的RSS源**：编辑 `rss_sources.md`
2. **改进筛选算法**：修改评分逻辑
3. **增加输出格式**：添加新的模板
4. **修复Bug**：提交问题报告

## 📄 许可证

本项目采用 MIT 许可证。

---

**提示**：首次运行时，系统会自动生成默认的 `config.yaml` 文件。请根据您的需求进行调整。