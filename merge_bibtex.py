#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
论文 BibTeX 合并和清理脚本
"""

import re
import os

def read_bibtex_file(filepath):
    """读取 BibTeX 文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def extract_entries(content):
    """提取所有 BibTeX 条目"""
    # 移除文件头
    content = re.sub(r'^---\s*---\s*', '', content, flags=re.MULTILINE)
    
    # 提取所有条目
    pattern = r'@\w+\{[^}]+,.*?\n\}'
    entries = re.findall(pattern, content, re.DOTALL)
    return entries

def get_entry_key(entry):
    """获取 BibTeX 条目的 key"""
    match = re.search(r'@\w+\{([^,]+),', entry)
    return match.group(1) if match else None

def merge_bibtex_files(original_file, new_file, output_file):
    """合并两个 BibTeX 文件，去重"""
    print("📖 读取原始文件...")
    original_content = read_bibtex_file(original_file)
    original_entries = extract_entries(original_content)
    
    print("📖 读取新文件...")
    new_content = read_bibtex_file(new_file)
    new_entries = extract_entries(new_content)
    
    # 收集已存在的 keys
    existing_keys = set()
    for entry in original_entries:
        key = get_entry_key(entry)
        if key:
            existing_keys.add(key)
    
    # 过滤新条目
    merged_entries = list(original_entries)
    added_count = 0
    
    print("\n📝 合并新论文...")
    for entry in new_entries:
        key = get_entry_key(entry)
        if key and key not in existing_keys:
            merged_entries.append(entry)
            existing_keys.add(key)
            added_count += 1
            # 提取标题
            title_match = re.search(r'title=\{([^}]+)\}', entry)
            title = title_match.group(1) if title_match else key
            print(f"  + {title[:60]}...")
        else:
            print(f"  - 跳过重复: {key}")
    
    # 写入合并后的文件
    print(f"\n💾 保存到 {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("---\n---\n\n")
        f.write('\n\n'.join(merged_entries))
        f.write('\n')
    
    print(f"\n✅ 完成！")
    print(f"  原始论文: {len(original_entries)} 篇")
    print(f"  新增论文: {added_count} 篇")
    print(f"  总计: {len(merged_entries)} 篇")
    
    return merged_entries

def create_placeholder_images(entries, img_dir):
    """为缺少预览图的论文创建占位符"""
    print("\n🖼️  检查预览图片...")
    
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    
    missing_images = []
    for entry in entries:
        preview_match = re.search(r'preview=\{([^}]+)\}', entry)
        if preview_match:
            img_name = preview_match.group(1)
            img_path = os.path.join(img_dir, img_name)
            
            if not os.path.exists(img_path):
                missing_images.append(img_name)
    
    if missing_images:
        print(f"\n⚠️  缺少 {len(missing_images)} 个预览图片:")
        for img in missing_images[:10]:  # 只显示前10个
            print(f"  - {img}")
        if len(missing_images) > 10:
            print(f"  ... 还有 {len(missing_images) - 10} 个")
        
        print(f"\n💡 提示:")
        print(f"  1. 可以从论文 PDF 截图作为预览图")
        print(f"  2. 保存到: {img_dir}")
        print(f"  3. 或者暂时使用占位图片")
    else:
        print("  ✅ 所有预览图片都已存在")

def list_missing_pdfs(entries):
    """列出缺少 PDF 链接的论文"""
    print("\n📄 检查 PDF 链接...")
    
    missing_pdfs = []
    for entry in entries:
        if 'ADD_PDF_LINK_HERE' in entry:
            title_match = re.search(r'title=\{([^}]+)\}', entry)
            title = title_match.group(1) if title_match else 'Unknown'
            missing_pdfs.append(title)
    
    if missing_pdfs:
        print(f"\n⚠️  需要添加 PDF 链接的论文 ({len(missing_pdfs)} 篇):")
        for i, title in enumerate(missing_pdfs[:5], 1):
            print(f"  {i}. {title[:70]}...")
        if len(missing_pdfs) > 5:
            print(f"  ... 还有 {len(missing_pdfs) - 5} 篇")
        
        print(f"\n💡 提示:")
        print(f"  1. 搜索并替换 'ADD_PDF_LINK_HERE' 为实际的 PDF 链接")
        print(f"  2. 可以使用 arXiv、CVF、IEEE 等链接")
    else:
        print("  ✅ 所有论文都有 PDF 链接")

def main():
    """主函数"""
    print("=" * 60)
    print("论文 BibTeX 合并工具")
    print("=" * 60)
    
    base_dir = '/Users/zinuo/Desktop/PhD/qiuhongke'
    original_file = os.path.join(base_dir, '_bibliography/papers.bib')
    new_file = os.path.join(base_dir, 'new_publications.bib')
    output_file = os.path.join(base_dir, '_bibliography/papers_merged.bib')
    img_dir = os.path.join(base_dir, 'assets/img/publication_preview')
    
    # 合并文件
    merged_entries = merge_bibtex_files(original_file, new_file, output_file)
    
    # 检查预览图片
    create_placeholder_images(merged_entries, img_dir)
    
    # 检查 PDF 链接
    list_missing_pdfs(merged_entries)
    
    print("\n" + "=" * 60)
    print("下一步:")
    print("  1. 检查 papers_merged.bib 文件内容")
    print("  2. 如果满意，运行:")
    print("     mv _bibliography/papers.bib _bibliography/papers.bib.backup")
    print("     mv _bibliography/papers_merged.bib _bibliography/papers.bib")
    print("  3. 添加缺失的预览图片")
    print("  4. 更新 PDF 链接")
    print("  5. 检查 keywords 和其他信息")
    print("=" * 60)

if __name__ == "__main__":
    main()

