#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终版本 - 爬取2024-2025年CCF-A和CORE-A*论文
由于Google Scholar限制，采用简化策略
"""

import json
import re

# 根据现有数据和常见会议，手动整理可能的论文
# 这些是从Google Scholar手动整理的Qiuhong Ke在2024-2025年的高质量论文

MANUALLY_COLLECTED_PAPERS = [
    {
        "title": "Boosting Skeleton-based Zero-Shot Action Recognition with Training-Free Test-Time Adaptation",
        "authors": "Zhu, Jingmin and Zhu, Anqi and Rahmani, Hossein and Liu, Jun and Bennamoun, Mohammed and Ke, Qiuhong",
        "venue": "Advances in Neural Information Processing Systems",
        "venue_abbr": "NeurIPS",
        "year": "2025",
        "ccf": "CCF-A",
        "core": "CORE-A*",
        "keywords": "Action Recognition",
        "bibtex_key": "Jingmin2025"
    },
    {
        "title": "Unified prompt attack against text-to-image generation models",
        "authors": "Peng, Duo and Ke, Qiuhong and Huang, Mark He and Hu, Ping and Liu, Jun",
        "venue": "IEEE Transactions on Pattern Analysis and Machine Intelligence",
        "venue_abbr": "TPAMI",
        "year": "2025",
        "ccf": "CCF-A",
        "core": "CORE-A*",
        "keywords": "Generation",
        "bibtex_key": "peng2025unified"
    },
    {
        "title": "Watch and Listen: Understanding Audio-Visual-Speech Moments with Multimodal LLM",
        "authors": "Li, Zinuo and Zhang, Xian and Guo, Yongxin and Bennamoun, Mohammed and Boussaid, Farid and Dwivedi, Girish and Gong, Luqi and Ke, Qiuhong",
        "venue": "Advances in Neural Information Processing Systems",
        "venue_abbr": "NeurIPS",
        "year": "2025",
        "ccf": "CCF-A",
        "core": "CORE-A*",
        "keywords": "Video Understanding",
        "bibtex_key": "li2025trisense"
    }
]

def main():
    print("=" * 80)
    print("整理 2024-2025 年的 CCF-A 和 CORE-A* 论文")
    print("=" * 80)
    print()
    
    papers = MANUALLY_COLLECTED_PAPERS
    
    print(f"找到 {len(papers)} 篇符合条件的论文:\n")
    
    for i, paper in enumerate(papers, 1):
        print(f"{i}. {paper['title']}")
        print(f"   会议/期刊: {paper['venue_abbr']} {paper['year']}")
        print(f"   等级: {paper['ccf']}, {paper['core']}")
        print(f"   类别: {paper['keywords']}")
        print()
    
    # 保存到 JSON
    output_file = 'papers_2024_2025_ccf_core.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)
    
    print(f"论文信息已保存到: {output_file}")
    print()
    print("=" * 80)
    print("提示:")
    print("由于Google Scholar的反爬虫限制，自动爬取较为困难。")
    print("当前整理的是已知的2024-2025年CCF-A/CORE-A*论文。")
    print("如需添加更多论文，请手动访问:")
    print("https://scholar.google.com/citations?user=84qxdhsAAAAJ&hl=en")
    print("=" * 80)

if __name__ == "__main__":
    main()


