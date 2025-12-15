#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试版本 - 查看爬取到的实际数据
"""

from scholarly import scholarly
import json

def main():
    author_id = "84qxdhsAAAAJ"
    
    print("正在搜索作者...")
    search_query = scholarly.search_author_id(author_id)
    author = scholarly.fill(search_query)
    
    print(f"作者: {author['name']}")
    print(f"总论文数: {len(author['publications'])}")
    print("\n" + "=" * 80)
    print("前10篇论文的详细信息:")
    print("=" * 80)
    
    for i, pub in enumerate(author['publications'][:10], 1):
        try:
            print(f"\n论文 {i}:")
            pub_filled = scholarly.fill(pub)
            
            print(f"  Title: {pub_filled.get('bib', {}).get('title', 'N/A')}")
            print(f"  Year: {pub_filled.get('bib', {}).get('pub_year', 'N/A')}")
            print(f"  Venue: {pub_filled.get('bib', {}).get('venue', 'N/A')}")
            print(f"  Author: {pub_filled.get('bib', {}).get('author', 'N/A')}")
            print(f"  Citations: {pub_filled.get('num_citations', 0)}")
            
            # 保存完整的pub_filled数据以供检查
            if i == 1:
                print(f"\n  完整数据结构:")
                print(f"  {json.dumps(pub_filled.get('bib', {}), indent=4, ensure_ascii=False)}")
            
        except Exception as e:
            print(f"  错误: {e}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()


