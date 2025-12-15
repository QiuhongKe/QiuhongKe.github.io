#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Scholar 论文爬取脚本 - 只获取 2024-2025 年的 CCF-A 和 CORE-A* 论文
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re

# CCF-A 和 CORE-A* 会议/期刊列表
CCF_A_VENUES = {
    # 会议
    'CVPR', 'ICCV', 'ECCV', 'NeurIPS', 'ICML', 'ICLR', 'AAAI', 'IJCAI',
    'ACM MM', 'SIGGRAPH', 'KDD', 'WWW', 'SIGIR', 'SIGMOD', 'VLDB',
    'ICDE', 'FOCS', 'STOC', 'SODA', 'CRYPTO', 'CCS', 'NDSS',
    # 期刊
    'TPAMI', 'TIP', 'IJCV', 'JMLR', 'TOG', 'TKDE', 'TODS', 'TOIS',
    'PIEEE', 'TC', 'JACM', 'TOCS', 'TSE', 'TOSEM'
}

CORE_A_STAR_VENUES = {
    'CVPR', 'ICCV', 'ECCV', 'NeurIPS', 'ICML', 'ICLR', 'AAAI', 'IJCAI',
    'ACM MM', 'SIGGRAPH', 'KDD', 'WWW', 'SIGIR', 'SIGMOD', 'VLDB',
    'ICDE', 'FOCS', 'STOC', 'SODA', 'CRYPTO', 'CCS', 'NDSS',
    'TPAMI', 'TIP', 'IJCV', 'JMLR', 'TOG', 'TKDE', 'TODS', 'TOIS'
}

def extract_year_from_text(text):
    """从文本中提取年份"""
    years = re.findall(r'\b(202[4-5])\b', text)
    return years[0] if years else None

def is_target_venue(venue_text):
    """判断是否为目标会议/期刊"""
    venue_upper = venue_text.upper()
    
    # 检查 CCF-A 和 CORE-A*
    for venue in CCF_A_VENUES.union(CORE_A_STAR_VENUES):
        if venue in venue_upper:
            return True, venue
    
    # 特殊匹配
    if 'IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE' in venue_upper:
        return True, 'TPAMI'
    if 'PATTERN ANALYSIS AND MACHINE INTELLIGENCE' in venue_upper:
        return True, 'TPAMI'
    if 'ADVANCES IN NEURAL INFORMATION PROCESSING' in venue_upper:
        return True, 'NeurIPS'
    if 'INTERNATIONAL CONFERENCE ON COMPUTER VISION' in venue_upper:
        return True, 'ICCV'
    if 'COMPUTER VISION AND PATTERN RECOGNITION' in venue_upper:
        return True, 'CVPR'
        
    return False, None

def scrape_scholar(url):
    """爬取 Google Scholar 个人主页"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    
    try:
        print(f"正在访问: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        papers = []
        
        # 查找所有论文条目
        paper_entries = soup.find_all('tr', class_='gsc_a_tr')
        
        print(f"找到 {len(paper_entries)} 篇论文")
        
        for entry in paper_entries:
            try:
                # 标题和链接
                title_elem = entry.find('a', class_='gsc_a_at')
                if not title_elem:
                    continue
                    
                title = title_elem.text.strip()
                
                # 作者和会议/期刊信息
                info_elem = entry.find('div', class_='gs_gray')
                authors = info_elem.text.strip() if info_elem else ""
                
                # 会议/期刊
                venue_elem = info_elem.find_next_sibling('div', class_='gs_gray') if info_elem else None
                venue = venue_elem.text.strip() if venue_elem else ""
                
                # 年份
                year_elem = entry.find('span', class_='gsc_a_h gsc_a_hc gs_ibl')
                year_text = year_elem.text.strip() if year_elem else ""
                year = extract_year_from_text(year_text) if year_text else None
                
                # 引用次数
                citation_elem = entry.find('a', class_='gsc_a_ac gs_ibl')
                citations = citation_elem.text.strip() if citation_elem and citation_elem.text.strip() else "0"
                
                # 检查年份是否为 2024 或 2025
                if not year or year not in ['2024', '2025']:
                    continue
                
                # 检查是否为目标会议/期刊
                is_target, venue_abbr = is_target_venue(venue)
                if not is_target:
                    continue
                
                paper_info = {
                    'title': title,
                    'authors': authors,
                    'venue': venue,
                    'venue_abbr': venue_abbr,
                    'year': year,
                    'citations': citations
                }
                
                papers.append(paper_info)
                print(f"✓ 找到目标论文: {title} ({venue_abbr}, {year}, 引用: {citations})")
                
            except Exception as e:
                print(f"解析论文条目时出错: {e}")
                continue
        
        return papers
        
    except requests.exceptions.RequestException as e:
        print(f"网络请求错误: {e}")
        return []
    except Exception as e:
        print(f"爬取过程中出错: {e}")
        return []

def main():
    url = "https://scholar.google.com/citations?user=84qxdhsAAAAJ&hl=en"
    
    print("=" * 60)
    print("开始爬取 Google Scholar 论文")
    print("筛选条件: 2024-2025年, CCF-A 或 CORE-A*")
    print("=" * 60)
    
    papers = scrape_scholar(url)
    
    if papers:
        # 按引用次数排序
        papers.sort(key=lambda x: int(x['citations']) if x['citations'].isdigit() else 0, reverse=True)
        
        print("\n" + "=" * 60)
        print(f"找到 {len(papers)} 篇符合条件的论文:")
        print("=" * 60)
        
        for i, paper in enumerate(papers, 1):
            print(f"\n{i}. {paper['title']}")
            print(f"   作者: {paper['authors']}")
            print(f"   会议/期刊: {paper['venue']} ({paper['venue_abbr']})")
            print(f"   年份: {paper['year']}")
            print(f"   引用: {paper['citations']}")
        
        # 保存到 JSON 文件
        output_file = 'scholar_papers_2024_2025.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(papers, f, ensure_ascii=False, indent=2)
        
        print(f"\n论文信息已保存到: {output_file}")
    else:
        print("\n未找到符合条件的论文")
        print("\n提示: Google Scholar 可能有反爬虫限制。")
        print("建议:")
        print("1. 手动访问页面并检查是否需要验证码")
        print("2. 使用浏览器的开发者工具复制 cookies")
        print("3. 或者使用 scholarly 库（需要安装: pip install scholarly）")

if __name__ == "__main__":
    main()


