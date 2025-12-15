#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 scholarly 库爬取 Google Scholar 论文 - 只获取 2024-2025 年的 CCF-A 和 CORE-A* 论文
"""

from scholarly import scholarly
import json
import re

# CCF-A 和 CORE-A* 会议/期刊列表
CCF_A_VENUES = {
    # 会议
    'CVPR', 'ICCV', 'ECCV', 'NeurIPS', 'ICML', 'ICLR', 'AAAI', 'IJCAI',
    'ACM MM', 'SIGGRAPH', 'KDD', 'WWW', 'SIGIR', 'SIGMOD', 'VLDB',
    'ICDE', 'FOCS', 'STOC', 'SODA', 'CRYPTO', 'CCS', 'NDSS', 'BMVC',
    # 期刊
    'TPAMI', 'TIP', 'IJCV', 'JMLR', 'TOG', 'TKDE', 'TODS', 'TOIS',
    'PIEEE', 'TC', 'JACM', 'TOCS', 'TSE', 'TOSEM', 'TMM'
}

CORE_A_STAR_VENUES = {
    'CVPR', 'ICCV', 'ECCV', 'NeurIPS', 'ICML', 'ICLR', 'AAAI', 'IJCAI',
    'ACM MM', 'SIGGRAPH', 'KDD', 'WWW', 'SIGIR', 'SIGMOD', 'VLDB',
    'ICDE', 'FOCS', 'STOC', 'SODA', 'CRYPTO', 'CCS', 'NDSS',
    'TPAMI', 'TIP', 'IJCV', 'JMLR', 'TOG', 'TKDE', 'TODS', 'TOIS'
}

def is_target_venue(venue_text):
    """判断是否为目标会议/期刊"""
    if not venue_text:
        return False, None
    
    venue_upper = venue_text.upper()
    
    # 检查 CCF-A 和 CORE-A*
    for venue in CCF_A_VENUES.union(CORE_A_STAR_VENUES):
        if venue in venue_upper:
            ccf = 'CCF-A' if venue in CCF_A_VENUES else None
            core = 'CORE-A*' if venue in CORE_A_STAR_VENUES else None
            return True, venue, ccf, core
    
    # 特殊匹配
    special_matches = {
        'IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE': ('TPAMI', 'CCF-A', 'CORE-A*'),
        'PATTERN ANALYSIS AND MACHINE INTELLIGENCE': ('TPAMI', 'CCF-A', 'CORE-A*'),
        'ADVANCES IN NEURAL INFORMATION PROCESSING': ('NeurIPS', 'CCF-A', 'CORE-A*'),
        'INTERNATIONAL CONFERENCE ON COMPUTER VISION': ('ICCV', 'CCF-A', 'CORE-A*'),
        'COMPUTER VISION AND PATTERN RECOGNITION': ('CVPR', 'CCF-A', 'CORE-A*'),
        'EUROPEAN CONFERENCE ON COMPUTER VISION': ('ECCV', 'CCF-A', 'CORE-A*'),
        'INTERNATIONAL CONFERENCE ON MACHINE LEARNING': ('ICML', 'CCF-A', 'CORE-A*'),
        'BRITISH MACHINE VISION CONFERENCE': ('BMVC', 'CCF-C', 'CORE-A'),
    }
    
    for pattern, (abbr, ccf, core) in special_matches.items():
        if pattern in venue_upper:
            return True, abbr, ccf, core
        
    return False, None, None, None

def scrape_scholar_author(author_id):
    """爬取指定作者的论文"""
    try:
        print(f"正在搜索作者 ID: {author_id}")
        
        # 搜索作者
        search_query = scholarly.search_author_id(author_id)
        author = scholarly.fill(search_query)
        
        print(f"找到作者: {author['name']}")
        print(f"总论文数: {len(author['publications'])}")
        
        papers = []
        
        for pub in author['publications']:
            try:
                # 填充论文详细信息
                pub_filled = scholarly.fill(pub)
                
                title = pub_filled.get('bib', {}).get('title', '')
                year = pub_filled.get('bib', {}).get('pub_year', '')
                venue = pub_filled.get('bib', {}).get('venue', '')
                authors = pub_filled.get('bib', {}).get('author', '')
                citations = pub_filled.get('num_citations', 0)
                
                # 检查年份
                if year not in ['2024', '2025']:
                    continue
                
                # 检查是否为目标会议/期刊
                is_target, venue_abbr, ccf, core = is_target_venue(venue)
                
                # 只保留 CCF-A 或 CORE-A* 的论文
                if not is_target or (ccf != 'CCF-A' and core != 'CORE-A*'):
                    continue
                
                paper_info = {
                    'title': title,
                    'authors': authors,
                    'venue': venue,
                    'venue_abbr': venue_abbr,
                    'year': year,
                    'citations': citations,
                    'ccf': ccf,
                    'core': core
                }
                
                papers.append(paper_info)
                print(f"✓ 找到目标论文: {title[:60]}... ({venue_abbr}, {year}, 引用: {citations})")
                
            except Exception as e:
                print(f"处理论文时出错: {e}")
                continue
        
        return papers
        
    except Exception as e:
        print(f"爬取过程中出错: {e}")
        return []

def main():
    author_id = "84qxdhsAAAAJ"
    
    print("=" * 80)
    print("使用 scholarly 库爬取 Google Scholar 论文")
    print("筛选条件: 2024-2025年, CCF-A 或 CORE-A*")
    print("=" * 80)
    print()
    
    papers = scrape_scholar_author(author_id)
    
    if papers:
        # 按引用次数排序
        papers.sort(key=lambda x: x['citations'], reverse=True)
        
        print("\n" + "=" * 80)
        print(f"找到 {len(papers)} 篇符合条件的论文:")
        print("=" * 80)
        
        for i, paper in enumerate(papers, 1):
            print(f"\n{i}. {paper['title']}")
            print(f"   作者: {paper['authors']}")
            print(f"   会议/期刊: {paper['venue']} ({paper['venue_abbr']})")
            print(f"   年份: {paper['year']}")
            print(f"   引用: {paper['citations']}")
            print(f"   等级: CCF={paper['ccf']}, CORE={paper['core']}")
        
        # 保存到 JSON 文件
        output_file = 'scholar_papers_2024_2025_ccf_core.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(papers, f, ensure_ascii=False, indent=2)
        
        print(f"\n论文信息已保存到: {output_file}")
    else:
        print("\n未找到符合条件的论文")

if __name__ == "__main__":
    main()


