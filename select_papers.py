#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从爬取的数据中选择高引用的CCF-A和CORE-A*论文
"""

import json
import re

# 读取爬取的数据
with open('scholar_papers.json', 'r', encoding='utf-8') as f:
    scholar_papers = json.load(f)

# 顶级会议和期刊（CCF-A 和 CORE-A*）
top_venues = ['CVPR', 'ICCV', 'NeurIPS', 'ICML', 'AAAI', 'IJCAI', 'ECCV', 'TPAMI', 'TIP']

# 选择顶会/顶刊论文
selected_papers = []
for paper in scholar_papers:
    venue = paper['venue']
    # 检查是否是顶会/顶刊
    is_top_venue = any(v in venue for v in top_venues)
    if is_top_venue:
        selected_papers.append(paper)
        print(f"✓ {paper['title'][:60]}... ({paper['year']}) - {paper['citations']} 引用")
    
    if len(selected_papers) >= 15:  # 多选几篇以备用
        break

print(f"\n总共选择了 {len(selected_papers)} 篇顶会/顶刊论文")
print("=" * 80)

# 保存选中的论文
with open('selected_papers.json', 'w', encoding='utf-8') as f:
    json.dump(selected_papers, f, ensure_ascii=False, indent=2)

print("已保存到 selected_papers.json")

