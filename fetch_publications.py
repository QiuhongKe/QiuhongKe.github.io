#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动从 Google Scholar 爬取论文并生成 BibTeX
"""

import re
import time
import requests
from bs4 import BeautifulSoup

# CCF-A 会议和期刊列表（部分常见的）
CCF_A_VENUES = {
    'CVPR', 'ICCV', 'ECCV', 'NeurIPS', 'ICML', 'ICLR', 'AAAI', 'IJCAI',
    'ACM MM', 'SIGGRAPH', 'KDD', 'WWW', 'SIGIR', 'SIGMOD', 'VLDB',
    'ICDE', 'OSDI', 'SOSP', 'NSDI', 'USENIX Security', 'CCS', 'NDSS',
    'S&P', 'FSE', 'ICSE', 'ASE', 'ISSTA', 'CHI', 'UbiComp', 'MobiCom',
    'MOBICOM', 'SIGCOMM', 'INFOCOM', 'RTSS', 'DATE', 'DAC',
    'TPAMI', 'TIP', 'TNNLS', 'TOG', 'TKDE', 'TOIS', 'TODS', 'VLDB J'
}

# CORE A* 会议和期刊列表（部分常见的）
CORE_ASTAR_VENUES = {
    'CVPR', 'ICCV', 'ECCV', 'NeurIPS', 'ICML', 'AAAI', 'IJCAI',
    'ACM MM', 'SIGGRAPH', 'KDD', 'WWW', 'SIGIR', 'SIGMOD', 'VLDB',
    'ICDE', 'OSDI', 'SOSP', 'CHI', 'MOBICOM', 'SIGCOMM', 'INFOCOM',
    'TPAMI', 'TKDE'
}


def fetch_google_scholar_page(user_id):
    """获取 Google Scholar 页面"""
    url = f"https://scholar.google.com/citations?user={user_id}&hl=en&cstart=0&pagesize=100"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"❌ 获取页面失败: {e}")
        return None


def parse_venue(pub_info):
    """从发表信息中提取会议/期刊名称"""
    # 常见格式: "Conference Name 2024" 或 "Journal Name, 2024"
    venue_patterns = [
        r'(CVPR|ICCV|ECCV|NeurIPS|ICML|ICLR|AAAI|IJCAI)',
        r'(ACM MM|SIGGRAPH|KDD|WWW|SIGIR)',
        r'(TPAMI|TIP|TNNLS|TKDE|BMVC)',
    ]
    
    for pattern in venue_patterns:
        match = re.search(pattern, pub_info, re.IGNORECASE)
        if match:
            return match.group(1).upper()
    return None


def determine_ccf_core(venue):
    """判断 CCF 和 CORE 等级"""
    if not venue:
        return None, None
    
    venue_upper = venue.upper()
    
    ccf = None
    core = None
    
    if venue_upper in CCF_A_VENUES:
        ccf = "CCF-A"
    
    if venue_upper in CORE_ASTAR_VENUES:
        core = "CORE-A*"
    elif venue_upper in CCF_A_VENUES:  # 如果是 CCF-A 但不是 CORE A*，可能是 CORE-A
        core = "CORE-A"
    
    return ccf, core


def parse_publications(html):
    """解析 Google Scholar 页面中的论文"""
    soup = BeautifulSoup(html, 'html.parser')
    papers = []
    
    # 查找所有论文条目
    paper_rows = soup.find_all('tr', class_='gsc_a_tr')
    
    for row in paper_rows:
        try:
            # 提取标题
            title_elem = row.find('a', class_='gsc_a_at')
            if not title_elem:
                continue
            title = title_elem.text.strip()
            
            # 提取作者
            authors_elem = row.find('div', class_='gs_gray')
            authors = authors_elem.text.strip() if authors_elem else ""
            
            # 提取发表信息（会议/期刊和年份）
            venue_elem = authors_elem.find_next_sibling('div', class_='gs_gray') if authors_elem else None
            venue_info = venue_elem.text.strip() if venue_elem else ""
            
            # 提取年份
            year_elem = row.find('span', class_='gsc_a_h')
            year = year_elem.text.strip() if year_elem else ""
            
            # 提取会议名称
            venue = parse_venue(venue_info)
            
            # 判断 CCF 和 CORE 等级
            ccf, core = determine_ccf_core(venue)
            
            # 只保留 CCF-A 或 CORE A* 的论文
            if ccf == "CCF-A" or core == "CORE-A*":
                papers.append({
                    'title': title,
                    'authors': authors,
                    'venue': venue or venue_info,
                    'year': year,
                    'ccf': ccf,
                    'core': core
                })
                print(f"✓ 找到: {title[:50]}... ({venue}, {year})")
        
        except Exception as e:
            print(f"⚠️  解析论文时出错: {e}")
            continue
    
    return papers


def generate_bibtex_key(authors, year, title):
    """生成 BibTeX key"""
    # 提取第一作者姓氏
    first_author = authors.split(',')[0].strip()
    last_name = first_author.split()[-1].lower()
    
    # 提取标题的第一个有意义的词
    title_words = re.findall(r'\w+', title.lower())
    title_word = title_words[0] if title_words else 'paper'
    
    return f"{last_name}{year}{title_word}"


def generate_bibtex(papers):
    """生成 BibTeX 格式"""
    bibtex_entries = []
    
    for paper in papers:
        key = generate_bibtex_key(paper['authors'], paper['year'], paper['title'])
        
        # 将作者格式转换为 BibTeX 格式
        authors = paper['authors'].replace(',', ' and')
        
        entry = f"""@article{{{key},
  title={{{paper['title']}}},
  author={{{authors}}},
  journal={{{paper['venue']}}},
  year={{{paper['year']}}},"""
        
        if paper.get('ccf'):
            entry += f"\n  ccf={{{paper['ccf']}}},"
        
        if paper.get('core'):
            entry += f"\n  core={{{paper['core']}}},"
        
        # 添加其他可能的字段
        venue_abbr = paper.get('venue', '').split()[0] if paper.get('venue') else None
        if venue_abbr and len(venue_abbr) > 2:
            entry += f"\n  abbr={{{venue_abbr}}},"
        
        # 添加 keywords 和 selected 标记
        entry += f"\n  selected={{true}},"
        entry += f"\n  keywords={{需要分类}},"
        entry += f"\n  preview={{需要添加图片.png}},"
        
        entry += "\n}\n"
        bibtex_entries.append(entry)
    
    return "\n".join(bibtex_entries)


def main():
    print("=" * 60)
    print("📚 Google Scholar 论文自动爬取工具")
    print("=" * 60)
    
    # 从 URL 中提取 user ID
    user_id = "84qxdhsAAAAJ"
    
    print(f"\n🔍 正在获取用户 {user_id} 的论文列表...")
    html = fetch_google_scholar_page(user_id)
    
    if not html:
        print("❌ 无法获取页面，请检查网络连接或稍后重试")
        return
    
    print("✓ 页面获取成功\n")
    print("📖 正在解析论文信息...\n")
    
    papers = parse_publications(html)
    
    if not papers:
        print("\n⚠️  未找到符合条件的论文（CCF-A 或 CORE A*）")
        print("可能原因：")
        print("  1. 会议名称格式无法识别")
        print("  2. Google Scholar 页面格式变化")
        print("  3. 需要手动添加更多会议到识别列表")
        return
    
    print(f"\n✅ 共找到 {len(papers)} 篇 CCF-A 或 CORE A* 论文\n")
    print("=" * 60)
    
    # 生成 BibTeX
    bibtex = generate_bibtex(papers)
    
    # 保存到文件
    output_file = "new_publications.bib"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("---\n---\n\n")
        f.write(bibtex)
    
    print(f"\n✅ BibTeX 已生成并保存到: {output_file}")
    print("\n📝 接下来的步骤:")
    print("  1. 查看 new_publications.bib 文件")
    print("  2. 修改 keywords（Action Recognition / Video Understanding / Generation）")
    print("  3. 添加预览图片到 assets/img/publication_preview/")
    print("  4. 添加 PDF、代码链接等")
    print("  5. 将内容复制到 _bibliography/papers.bib")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()

