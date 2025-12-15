#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爬取 Google Scholar 个人主页的论文信息
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time

def scrape_scholar_profile(user_id, max_papers=50):
    """
    爬取 Google Scholar 个人主页
    """
    url = f"https://scholar.google.com/citations?user={user_id}&hl=en&cstart=0&pagesize=100"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }
    
    try:
        print(f"正在访问: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有论文条目
        papers = []
        paper_rows = soup.find_all('tr', class_='gsc_a_tr')
        
        print(f"找到 {len(paper_rows)} 篇论文")
        
        for idx, row in enumerate(paper_rows[:max_papers]):
            try:
                # 提取论文信息
                title_elem = row.find('a', class_='gsc_a_at')
                if not title_elem:
                    continue
                    
                title = title_elem.text.strip()
                
                # 提取作者和会议/期刊信息
                authors_elem = row.find('div', class_='gs_gray')
                authors = authors_elem.text.strip() if authors_elem else ""
                
                # 提取会议/期刊
                venue_elem = authors_elem.find_next_sibling('div', class_='gs_gray') if authors_elem else None
                venue = venue_elem.text.strip() if venue_elem else ""
                
                # 提取引用数
                cited_elem = row.find('a', class_='gsc_a_ac')
                citations = cited_elem.text.strip() if cited_elem and cited_elem.text.strip() else "0"
                citations = int(citations) if citations.isdigit() else 0
                
                # 提取年份
                year_elem = row.find('span', class_='gsc_a_h')
                year = year_elem.text.strip() if year_elem else ""
                
                paper_info = {
                    'title': title,
                    'authors': authors,
                    'venue': venue,
                    'citations': citations,
                    'year': year
                }
                
                papers.append(paper_info)
                print(f"{idx+1}. {title} ({year}) - {citations} 引用")
                
            except Exception as e:
                print(f"解析论文 {idx+1} 时出错: {e}")
                continue
        
        # 按引用数排序
        papers.sort(key=lambda x: x['citations'], reverse=True)
        
        return papers
        
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return []
    except Exception as e:
        print(f"发生错误: {e}")
        return []

def main():
    user_id = "84qxdhsAAAAJ"
    
    print("=" * 60)
    print("开始爬取 Google Scholar...")
    print("=" * 60)
    
    papers = scrape_scholar_profile(user_id)
    
    if papers:
        print("\n" + "=" * 60)
        print(f"成功获取 {len(papers)} 篇论文")
        print("=" * 60)
        print("\n引用数最高的前10篇:")
        for i, paper in enumerate(papers[:10], 1):
            print(f"\n{i}. {paper['title']}")
            print(f"   引用数: {paper['citations']}")
            print(f"   年份: {paper['year']}")
            print(f"   会议/期刊: {paper['venue']}")
        
        # 保存为 JSON
        output_file = 'scholar_papers.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(papers, f, ensure_ascii=False, indent=2)
        print(f"\n所有论文数据已保存到: {output_file}")
        
    else:
        print("\n未能获取论文数据")

if __name__ == "__main__":
    main()

