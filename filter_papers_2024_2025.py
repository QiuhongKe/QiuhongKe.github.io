#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
筛选2024-2025年的CCF-A和CORE-A*论文
"""

import json
import re

# CCF-A 会议/期刊列表
CCF_A_VENUES = {
    'CVPR', 'ICCV', 'ECCV', 'NeurIPS', 'ICML', 'ICLR', 'AAAI', 'IJCAI',
    'ACM MM', 'MM', 'SIGGRAPH', 'TPAMI', 'TIP', 'IJCV', 'TOG', 'TMI'
}

# CORE-A* 会议/期刊列表
CORE_A_STAR_VENUES = {
    'CVPR', 'ICCV', 'ECCV', 'NeurIPS', 'ICML', 'ICLR', 'AAAI', 'IJCAI',
    'ACM MM', 'SIGGRAPH', 'TPAMI', 'IJCV', 'TOG', 'KDD'
}

def classify_venue(venue_str):
    """
    根据venue字符串判断是否是CCF-A或CORE-A*
    """
    venue_upper = venue_str.upper()
    
    ccf_a = False
    core_a_star = False
    
    # 检查CCF-A
    for v in CCF_A_VENUES:
        if v.upper() in venue_upper:
            ccf_a = True
            break
    
    # 检查CORE-A*
    for v in CORE_A_STAR_VENUES:
        if v.upper() in venue_upper:
            core_a_star = True
            break
    
    # 特殊处理TPAMI (IEEE TPAMI)
    if 'PATTERN ANALYSIS' in venue_upper and 'MACHINE INTELLIGENCE' in venue_upper:
        ccf_a = True
        core_a_star = True
    
    # 特殊处理TIP
    if 'IEEE TRANSACTIONS ON IMAGE PROCESSING' in venue_upper or 'IEEE TRANS' in venue_upper and 'IMAGE' in venue_upper:
        ccf_a = True
    
    return ccf_a, core_a_star

def extract_abbr_from_venue(venue_str):
    """
    从venue字符串中提取会议/期刊缩写
    """
    venue_upper = venue_str.upper()
    
    # 常见缩写映射
    abbr_map = {
        'CVPR': 'CVPR',
        'ICCV': 'ICCV', 
        'ECCV': 'ECCV',
        'NEURIPS': 'NeurIPS',
        'NIPS': 'NeurIPS',
        'ICML': 'ICML',
        'ICLR': 'ICLR',
        'AAAI': 'AAAI',
        'IJCAI': 'IJCAI',
        'ACM MM': 'ACM MM',
        'SIGGRAPH': 'SIGGRAPH',
        'TPAMI': 'TPAMI',
        'IJCV': 'IJCV',
        'TIP': 'TIP',
        'TOG': 'TOG',
        'WACV': 'WACV',
        'BMVC': 'BMVC'
    }
    
    for key, value in abbr_map.items():
        if key in venue_upper:
            return value
    
    # 特殊处理TPAMI
    if 'PATTERN ANALYSIS' in venue_upper and 'MACHINE INTELLIGENCE' in venue_upper:
        return 'TPAMI'
    
    # 特殊处理TIP
    if 'IMAGE PROCESSING' in venue_upper:
        return 'TIP'
    
    return 'Unknown'

def generate_bibtex_key(authors, year):
    """
    生成BibTeX key
    """
    # 提取第一作者的姓
    first_author = authors.split(',')[0].strip()
    last_name = first_author.split()[-1].lower()
    
    return f"{last_name}{year}"

def determine_keywords(title, venue):
    """
    根据标题和venue确定关键词类别
    """
    title_lower = title.lower()
    
    # Generation相关
    if any(word in title_lower for word in ['generation', 'synthesis', 'diffusion', 'gan', 'text-to-image', 'pose estimation', 'inpainting', 'completion', 'attack', 'adversarial']):
        return 'Generation'
    
    # Video Understanding相关
    if any(word in title_lower for word in ['video', 'temporal', 'summarization', 'question answering', 'multimodal', 'audio-visual']):
        return 'Video Understanding'
    
    # Action Recognition相关
    if any(word in title_lower for word in ['action', 'skeleton', 'pose', 'motion', 'activity', 'gesture']):
        return 'Action Recognition'
    
    return 'Action Recognition'  # 默认

def main():
    # 读取爬取的数据
    with open('scholar_papers.json', 'r', encoding='utf-8') as f:
        papers = json.load(f)
    
    print("=" * 80)
    print("筛选2024-2025年的CCF-A和CORE-A*论文")
    print("=" * 80)
    
    # 筛选2024-2025年的论文
    filtered_papers = []
    for paper in papers:
        year = paper.get('year', '')
        if year in ['2024', '2025']:
            ccf_a, core_a_star = classify_venue(paper['venue'])
            if ccf_a and core_a_star:
                paper['ccf'] = 'CCF-A'
                paper['core'] = 'CORE-A*'
                paper['abbr'] = extract_abbr_from_venue(paper['venue'])
                paper['keywords'] = determine_keywords(paper['title'], paper['venue'])
                filtered_papers.append(paper)
                print(f"\n✓ {paper['title']}")
                print(f"  年份: {year} | 会议: {paper['abbr']} | 引用: {paper['citations']}")
    
    print(f"\n{'=' * 80}")
    print(f"共找到 {len(filtered_papers)} 篇2024-2025年的CCF-A和CORE-A*论文")
    print("=" * 80)
    
    # 按引用数排序
    filtered_papers.sort(key=lambda x: x['citations'], reverse=True)
    
    # 生成BibTeX条目
    print("\n\n开始生成BibTeX条目...\n")
    print("=" * 80)
    
    bibtex_entries = []
    for paper in filtered_papers:
        key = generate_bibtex_key(paper['authors'], paper['year'])
        
        # 清理标题中的特殊字符
        title = paper['title'].replace('{', '').replace('}', '')
        
        # 确定entry类型
        venue_lower = paper['venue'].lower()
        if 'conference' in venue_lower or 'proceedings' in venue_lower or paper['abbr'] in ['CVPR', 'ICCV', 'ECCV', 'NeurIPS', 'ICML', 'ICLR', 'AAAI', 'IJCAI', 'WACV', 'BMVC']:
            entry_type = 'inproceedings'
            venue_field = f"  booktitle={{{paper['venue']}}},"
        else:
            entry_type = 'article'
            venue_field = f"  journal={{{paper['venue']}}},"
        
        bibtex = f"""@{entry_type}{{{key},
  title={{{title}}},
  author={{{paper['authors']}}},
{venue_field}
  abbr={{{paper['abbr']}}},
  ccf={{{paper['ccf']}}},
  core={{{paper['core']}}},
  year={{{paper['year']}}},
  keywords={{{paper['keywords']}}},
  preview={{{key}.png}}
}}"""
        
        bibtex_entries.append(bibtex)
        print(bibtex)
        print()
    
    # 保存到文件
    output_file = 'new_papers_2024_2025.bib'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(bibtex_entries))
    
    print("=" * 80)
    print(f"BibTeX条目已保存到: {output_file}")
    print("=" * 80)

if __name__ == "__main__":
    main()

