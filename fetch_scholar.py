#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Scholar 论文信息爬取脚本
自动获取论文信息并生成 BibTeX 格式
"""

import re
import time
import urllib.request
import urllib.parse
from html.parser import HTMLParser
import json

class ScholarParser(HTMLParser):
    """解析 Google Scholar HTML"""
    def __init__(self):
        super().__init__()
        self.papers = []
        self.current_paper = {}
        self.in_title = False
        self.in_authors = False
        self.in_venue = False
        self.in_year = False
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # 论文标题
        if tag == 'a' and attrs_dict.get('class') == 'gsc_a_at':
            self.in_title = True
            
        # 作者信息
        if tag == 'div' and 'gs_gray' in attrs_dict.get('class', ''):
            if not self.current_paper.get('authors'):
                self.in_authors = True
            elif not self.current_paper.get('venue'):
                self.in_venue = True
    
    def handle_data(self, data):
        data = data.strip()
        if not data:
            return
            
        if self.in_title:
            self.current_paper['title'] = data
            self.in_title = False
            
        if self.in_authors:
            self.current_paper['authors'] = data
            self.in_authors = False
            
        if self.in_venue:
            self.current_paper['venue'] = data
            self.in_venue = False
            # 提取年份
            year_match = re.search(r'\b(19|20)\d{2}\b', data)
            if year_match:
                self.current_paper['year'] = year_match.group()
                
    def handle_endtag(self, tag):
        if tag == 'tr' and self.current_paper:
            if 'title' in self.current_paper:
                self.papers.append(self.current_paper)
                self.current_paper = {}


def fetch_google_scholar(user_id):
    """获取 Google Scholar 个人页面"""
    url = f"https://scholar.google.com/citations?user={user_id}&hl=en&cstart=0&pagesize=100"
    
    print(f"正在获取 Google Scholar 数据...")
    print(f"URL: {url}")
    
    try:
        # 添加 User-Agent 避免被拒绝
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8')
            return html
    except Exception as e:
        print(f"❌ 获取失败: {e}")
        return None


def parse_papers(html):
    """解析论文信息"""
    parser = ScholarParser()
    parser.feed(html)
    return parser.papers


def guess_venue_info(venue_text):
    """根据会议/期刊名称猜测 CCF/CORE 等级和缩写"""
    venue_text_upper = venue_text.upper()
    
    # 顶级会议/期刊映射
    top_venues = {
        'CVPR': {'abbr': 'CVPR', 'ccf': 'CCF-A', 'core': 'CORE-A*', 'full': 'Conference on Computer Vision and Pattern Recognition'},
        'ICCV': {'abbr': 'ICCV', 'ccf': 'CCF-A', 'core': 'CORE-A*', 'full': 'International Conference on Computer Vision'},
        'ECCV': {'abbr': 'ECCV', 'ccf': 'CCF-B', 'core': 'CORE-A', 'full': 'European Conference on Computer Vision'},
        'NEURIPS': {'abbr': 'NeurIPS', 'ccf': 'CCF-A', 'core': 'CORE-A*', 'full': 'Advances in Neural Information Processing Systems'},
        'NIPS': {'abbr': 'NeurIPS', 'ccf': 'CCF-A', 'core': 'CORE-A*', 'full': 'Neural Information Processing Systems'},
        'ICML': {'abbr': 'ICML', 'ccf': 'CCF-A', 'core': 'CORE-A*', 'full': 'International Conference on Machine Learning'},
        'AAAI': {'abbr': 'AAAI', 'ccf': 'CCF-A', 'core': 'CORE-A*', 'full': 'AAAI Conference on Artificial Intelligence'},
        'IJCAI': {'abbr': 'IJCAI', 'ccf': 'CCF-A', 'core': 'CORE-A*', 'full': 'International Joint Conference on Artificial Intelligence'},
        'ACM MM': {'abbr': 'ACM MM', 'ccf': 'CCF-A', 'core': 'CORE-A*', 'full': 'ACM International Conference on Multimedia'},
        'SIGGRAPH': {'abbr': 'SIGGRAPH', 'ccf': 'CCF-A', 'core': 'CORE-A*', 'full': 'ACM SIGGRAPH'},
        'BMVC': {'abbr': 'BMVC', 'ccf': 'CCF-C', 'core': 'CORE-A', 'full': 'British Machine Vision Conference'},
        'WACV': {'abbr': 'WACV', 'ccf': 'CCF-C', 'core': 'CORE-B', 'full': 'Winter Conference on Applications of Computer Vision'},
        'TPAMI': {'abbr': 'TPAMI', 'ccf': 'CCF-A', 'core': 'CORE-A*', 'full': 'IEEE Transactions on Pattern Analysis and Machine Intelligence'},
        'IJCV': {'abbr': 'IJCV', 'ccf': 'CCF-A', 'core': 'CORE-A*', 'full': 'International Journal of Computer Vision'},
        'TIP': {'abbr': 'TIP', 'ccf': 'CCF-A', 'core': 'CORE-A', 'full': 'IEEE Transactions on Image Processing'},
        'TMM': {'abbr': 'TMM', 'ccf': 'CCF-B', 'core': 'CORE-A', 'full': 'IEEE Transactions on Multimedia'},
        'TCSVT': {'abbr': 'TCSVT', 'ccf': 'CCF-B', 'core': 'CORE-B', 'full': 'IEEE Transactions on Circuits and Systems for Video Technology'},
    }
    
    for key, info in top_venues.items():
        if key in venue_text_upper or info['full'].upper() in venue_text_upper:
            return info
    
    return None


def generate_bibtex_key(authors, year, title):
    """生成 BibTeX key"""
    # 提取第一作者姓氏
    first_author = authors.split(',')[0].strip()
    last_name = first_author.split()[-1].lower()
    
    # 提取标题首个有意义的词
    title_words = re.findall(r'\b[A-Za-z]+\b', title)
    title_word = title_words[0].lower() if title_words else 'paper'
    
    return f"{last_name}{year}{title_word}"


def guess_keywords(title, venue):
    """根据标题和会议猜测关键词"""
    title_lower = title.lower()
    venue_lower = venue.lower() if venue else ''
    
    keywords = []
    
    # Action Recognition
    if any(word in title_lower for word in ['action', 'activity', 'skeleton', 'gesture']):
        keywords.append('Action Recognition')
    
    # Video Understanding
    if any(word in title_lower for word in ['video', 'temporal', 'frame', 'clip']):
        keywords.append('Video Understanding')
    
    # Generation
    if any(word in title_lower for word in ['generation', 'synthesis', 'gan', 'diffusion', 'generative']):
        keywords.append('Generation')
    
    # 默认关键词
    if not keywords:
        keywords.append('Computer Vision')
    
    return ', '.join(keywords)


def format_bibtex(paper):
    """格式化为 BibTeX"""
    venue_info = guess_venue_info(paper.get('venue', ''))
    
    # 只处理 CCF-A 或 CORE-A* 的论文
    if not venue_info:
        return None
    if 'CCF-A' not in venue_info['ccf'] and 'CORE-A*' not in venue_info['core']:
        return None
    
    key = generate_bibtex_key(
        paper.get('authors', 'Unknown'),
        paper.get('year', '2024'),
        paper.get('title', 'Untitled')
    )
    
    # 生成作者列表
    authors = paper.get('authors', '').replace(' and ', ', ')
    
    # 猜测关键词
    keywords = guess_keywords(paper.get('title', ''), paper.get('venue', ''))
    
    bibtex = f"""@article{{{key},
  title={{{paper.get('title', 'Untitled')}}},
  author={{{authors}}},
  journal={{{venue_info['full']}}},
  abbr={{{venue_info['abbr']}}},
  ccf={{{venue_info['ccf']}}},
  core={{{venue_info['core']}}},
  keywords={{{keywords}}},
  year={{{paper.get('year', '2024')}}},
  preview={{{key}.png}},
  pdf={{ADD_PDF_LINK_HERE}},
}}
"""
    return bibtex


def main():
    """主函数"""
    print("=" * 60)
    print("Google Scholar 论文信息爬取工具")
    print("=" * 60)
    
    # 从 URL 提取 user_id
    user_id = "84qxdhsAAAAJ"
    
    # 获取 HTML
    html = fetch_google_scholar(user_id)
    if not html:
        print("❌ 无法获取 Google Scholar 数据")
        return
    
    # 解析论文
    papers = parse_papers(html)
    print(f"\n✅ 找到 {len(papers)} 篇论文\n")
    
    # 生成 BibTeX
    bibtex_entries = []
    filtered_count = 0
    
    for i, paper in enumerate(papers, 1):
        print(f"[{i}/{len(papers)}] {paper.get('title', 'Unknown')[:60]}...")
        
        bibtex = format_bibtex(paper)
        if bibtex:
            bibtex_entries.append(bibtex)
            filtered_count += 1
            venue_info = guess_venue_info(paper.get('venue', ''))
            print(f"  ✓ {venue_info['abbr']} - {venue_info['ccf']} / {venue_info['core']}")
        else:
            print(f"  - 跳过（不是 CCF-A 或 CORE-A*）")
    
    # 保存结果
    if bibtex_entries:
        output_file = '/Users/zinuo/Desktop/PhD/qiuhongke/new_publications.bib'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("---\n---\n\n")
            f.write('\n'.join(bibtex_entries))
        
        print(f"\n" + "=" * 60)
        print(f"✅ 成功生成 {filtered_count} 篇 CCF-A/CORE-A* 论文的 BibTeX")
        print(f"📁 已保存到: {output_file}")
        print(f"\n⚠️  请注意:")
        print(f"  1. 检查作者姓名是否正确")
        print(f"  2. 添加 PDF 链接 (搜索 ADD_PDF_LINK_HERE)")
        print(f"  3. 添加预览图片到 assets/img/publication_preview/")
        print(f"  4. 检查关键词是否合适")
        print(f"  5. 可选: 添加 code, website 等链接")
        print("=" * 60)
    else:
        print("\n❌ 没有找到符合条件的论文")


if __name__ == "__main__":
    main()

