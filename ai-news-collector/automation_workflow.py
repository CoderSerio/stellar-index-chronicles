#!/usr/bin/env python3
"""
AI趋势新闻收集使徒 - 自动化工作流
"""

import feedparser
import requests
from datetime import datetime, timedelta
import json
import os
import re
from typing import List, Dict, Any
import yaml
from jinja2 import Template

class AINewsCollector:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self.load_config(config_path)
        self.rss_sources = self.load_rss_sources()
        self.filter_criteria = self.load_filter_criteria()
        
    def load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        else:
            return self.create_default_config()
    
    def create_default_config(self) -> Dict:
        """创建默认配置"""
        default_config = {
            'output_dir': './output',
            'cache_dir': './cache',
            'update_interval_hours': 1,
            'daily_summary_time': '09:00',
            'weekly_summary_day': 'monday',
            'max_articles_per_source': 10,
            'min_score_threshold': 3.5,
            'notification_channels': ['file', 'telegram']
        }
        with open('config.yaml', 'w', encoding='utf-8') as f:
            yaml.dump(default_config, f, allow_unicode=True)
        return default_config
    
    def load_rss_sources(self) -> List[Dict]:
        """加载RSS源列表"""
        sources = []
        if os.path.exists('rss_sources.md'):
            with open('rss_sources.md', 'r', encoding='utf-8') as f:
                content = f.read()
                # 解析Markdown表格
                lines = content.split('\n')
                in_table = False
                headers = []
                for line in lines:
                    if line.strip().startswith('|') and 'URL' in line:
                        headers = [h.strip() for h in line.split('|')[1:-1]]
                        in_table = True
                        continue
                    if in_table and line.strip().startswith('|') and not line.strip().startswith('|---'):
                        values = [v.strip() for v in line.split('|')[1:-1]]
                        if len(values) == len(headers):
                            source = dict(zip(headers, values))
                            sources.append({
                                'name': source.get('来源名称', ''),
                                'url': source.get('RSS URL', ''),
                                'category': source.get('主要分类', ''),
                                'priority': int(source.get('优先级', 3)),
                                'language': source.get('语言', 'zh')
                            })
        return sources
    
    def load_filter_criteria(self) -> Dict:
        """加载筛选标准"""
        criteria = {
            'exclude_keywords': [],
            'priority_keywords': [],
            'min_score_threshold': 3.5
        }
        
        if os.path.exists('news_filter_criteria.md'):
            with open('news_filter_criteria.md', 'r', encoding='utf-8') as f:
                content = f.read()
                # 提取排除关键词
                exclude_match = re.search(r'exclude_keywords:\s*\[(.*?)\]', content, re.DOTALL)
                if exclude_match:
                    criteria['exclude_keywords'] = [kw.strip().strip('"\'') 
                                                  for kw in exclude_match.group(1).split(',')]
                
                # 提取优先关键词  
                priority_match = re.search(r'priority_keywords:\s*\[(.*?)\]', content, re.DOTALL)
                if priority_match:
                    criteria['priority_keywords'] = [kw.strip().strip('"\'') 
                                                   for kw in priority_match.group(1).split(',')]
        
        return criteria
    
    def fetch_rss_feeds(self) -> List[Dict]:
        """获取所有RSS源的文章"""
        all_articles = []
        
        for source in self.rss_sources:
            try:
                print(f"正在获取 {source['name']} 的文章...")
                feed = feedparser.parse(source['url'])
                
                for entry in feed.entries[:self.config['max_articles_per_source']]:
                    article = {
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'summary': entry.get('summary', ''),
                        'published': entry.get('published', ''),
                        'source': source['name'],
                        'category': source['category'],
                        'priority': source['priority']
                    }
                    all_articles.append(article)
                    
            except Exception as e:
                print(f"获取 {source['name']} 失败: {e}")
                continue
        
        return all_articles
    
    def calculate_article_score(self, article: Dict) -> float:
        """计算文章评分"""
        score = 0.0
        max_score = 5.0
        
        # 检查排除关键词
        title_lower = article['title'].lower()
        summary_lower = article['summary'].lower()
        full_text = title_lower + ' ' + summary_lower
        
        for keyword in self.filter_criteria['exclude_keywords']:
            if keyword.lower() in full_text:
                return 0.0  # 直接排除
        
        # 商业价值评分 (30%)
        business_score = self.evaluate_business_value(article)
        score += business_score * 0.3
        
        # 技术深度评分 (25%)
        tech_score = self.evaluate_technical_depth(article)
        score += tech_score * 0.25
        
        # 创新性评分 (20%)
        innovation_score = self.evaluate_innovation(article)
        score += innovation_score * 0.2
        
        # 实用性评分 (15%)
        practical_score = self.evaluate_practicality(article)
        score += practical_score * 0.15
        
        # 来源可信度 (10%)
        credibility_score = min(article['priority'], 5.0)
        score += credibility_score * 0.1
        
        return min(score, max_score)
    
    def evaluate_business_value(self, article: Dict) -> float:
        """评估商业价值"""
        text = article['title'] + ' ' + article['summary']
        keywords = ['案例', 'ROI', '成本', '效率', '收入', '商业化', '企业', '部署', '生产']
        score = sum(1 for kw in keywords if kw in text)
        return min(score * 1.0, 5.0)
    
    def evaluate_technical_depth(self, article: Dict) -> float:
        """评估技术深度"""
        text = article['title'] + ' ' + article['summary']
        keywords = ['代码', '实现', '架构', '算法', '性能', 'benchmark', '优化', '调试']
        score = sum(1 for kw in keywords if kw in text)
        return min(score * 1.25, 5.0)
    
    def evaluate_innovation(self, article: Dict) -> float:
        """评估创新性"""
        text = article['title'] + ' ' + article['summary']
        keywords = ['新', '突破', '首创', '创新', '首次', '发布', '开源', 'SOTA']
        score = sum(1 for kw in keywords if kw in text)
        return min(score * 1.25, 5.0)
    
    def evaluate_practicality(self, article: Dict) -> float:
        """评估实用性"""
        text = article['title'] + ' ' + article['summary']
        keywords = ['教程', '指南', '最佳实践', '工具', '框架', 'API', '集成', '自动化']
        score = sum(1 for kw in keywords if kw in text)
        return min(score * 1.67, 5.0)
    
    def filter_and_rank_articles(self, articles: List[Dict]) -> List[Dict]:
        """筛选和排序文章"""
        scored_articles = []
        
        for article in articles:
            score = self.calculate_article_score(article)
            if score >= self.config['min_score_threshold']:
                article['score'] = score
                scored_articles.append(article)
        
        # 按分数降序排序
        scored_articles.sort(key=lambda x: x['score'], reverse=True)
        return scored_articles
    
    def generate_daily_summary(self, articles: List[Dict]) -> str:
        """生成每日简报"""
        today = datetime.now().strftime('%Y-%m-%d')
        template_path = 'content_template.md'
        
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
                # 提取每日简报模板部分
                daily_template_match = re.search(r'## 每日简报模板\n```markdown\n(.*?)```', 
                                               template_content, re.DOTALL)
                if daily_template_match:
                    template_str = daily_template_match.group(1)
                    template = Template(template_str)
                    
                    # 准备数据
                    business_articles = [a for a in articles if '商业' in a.get('category', '')]
                    tech_articles = [a for a in articles if '技术' in a.get('category', '') or '研发' in a.get('category', '')]
                    
                    context = {
                        '日期': today,
                        '精选文章数量': len(articles),
                        '总文章数量': len(articles) * 2,  # 假设原始数量是精选的2倍
                        '亮点文章': articles[0] if articles else None,
                        '商业应用文章': business_articles[:3],
                        '研发提效文章': tech_articles[:3],
                        '生成时间': datetime.now().strftime('%Y-%m-%d %H:%M')
                    }
                    
                    return template.render(**context)
        
        return f"# AI趋势日报 - {today}\n\n今日无符合条件的文章。"
    
    def save_output(self, content: str, filename: str):
        """保存输出文件"""
        output_dir = self.config['output_dir']
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"已保存到: {filepath}")
    
    def run_daily_collection(self):
        """运行每日收集任务"""
        print("开始AI趋势新闻收集...")
        
        # 获取文章
        articles = self.fetch_rss_feeds()
        print(f"获取到 {len(articles)} 篇文章")
        
        # 筛选和评分
        filtered_articles = self.filter_and_rank_articles(articles)
        print(f"筛选后剩余 {len(filtered_articles)} 篇高质量文章")
        
        # 生成每日简报
        daily_summary = self.generate_daily_summary(filtered_articles)
        
        # 保存输出
        today = datetime.now().strftime('%Y-%m-%d')
        self.save_output(daily_summary, f'daily_summary_{today}.md')
        
        # 保存详细文章列表
        detailed_list = self.generate_detailed_list(filtered_articles)
        self.save_output(detailed_list, f'detailed_articles_{today}.json')
        
        print("每日收集任务完成！")
    
    def generate_detailed_list(self, articles: List[Dict]) -> str:
        """生成详细文章列表（JSON格式）"""
        return json.dumps(articles, ensure_ascii=False, indent=2)

def main():
    """主函数"""
    collector = AINewsCollector()
    collector.run_daily_collection()

if __name__ == "__main__":
    main()