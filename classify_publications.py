#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
辅助脚本：帮助分类论文并添加更多信息
"""

import re

# 关键词分类规则
CLASSIFICATION_RULES = {
    'Action Recognition': [
        'action', 'activity', 'skeleton', 'gesture', 'behavior', 
        'human motion', 'pose estimation', 'interaction recognition'
    ],
    'Video Understanding': [
        'video', 'temporal', 'anticipation', 'prediction', 
        'spatio-temporal', 'early action', 'multimodal'
    ],
    'Generation': [
        'generation', 'synthesis', 'diffusion', 'gan', 'generative',
        'text-to-image', 'video generation', 'completion'
    ],
    '3D Vision': [
        '3d', 'point cloud', 'shape', 'rotation', 'depth', 'amodal'
    ],
    'Domain Adaptation': [
        'domain adaptation', 'transfer learning', 'unsupervised',
        'cross-domain', 'zero-shot'
    ],
    'Adversarial': [
        'adversarial', 'attack', 'robust', 'security', 'noise'
    ]
}


def classify_paper(title):
    """根据标题自动分类论文"""
    title_lower = title.lower()
    categories = []
    
    for category, keywords in CLASSIFICATION_RULES.items():
        for keyword in keywords:
            if keyword in title_lower:
                categories.append(category)
                break
    
    # 如果没有匹配到，返回默认分类
    if not categories:
        return ['Action Recognition']  # 默认分类
    
    # 返回最相关的分类
    return categories[:1]  # 只返回第一个匹配的分类


def process_bibtex_file(input_file, output_file):
    """处理 BibTeX 文件，自动分类并添加建议"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 分割每个条目
    entries = re.split(r'\n@', content)
    
    processed_entries = []
    
    for i, entry in enumerate(entries):
        if not entry.strip():
            continue
            
        # 恢复 @ 符号
        if not entry.startswith('@'):
            entry = '@' + entry
        
        # 提取标题
        title_match = re.search(r'title=\{([^}]+)\}', entry)
        if not title_match:
            processed_entries.append(entry)
            continue
        
        title = title_match.group(1)
        categories = classify_paper(title)
        
        # 替换 keywords
        category_str = ', '.join(categories)
        entry = re.sub(
            r'keywords=\{需要分类\}',
            f'keywords={{{category_str}}}',
            entry
        )
        
        # 生成预览图片文件名建议
        key_match = re.search(r'@article\{([^,]+)', entry)
        if key_match:
            key = key_match.group(1)
            preview_name = f"{key}.png"
            entry = re.sub(
                r'preview=\{需要添加图片\.png\}',
                f'preview={{{preview_name}}}',
                entry
            )
            entry += f"\n  // 建议: 添加图片 {preview_name} 到 assets/img/publication_preview/\n"
        
        processed_entries.append(entry)
        
        # 打印分类结果
        print(f"✓ [{category_str}] {title[:60]}...")
    
    # 写入处理后的文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('---\n---\n\n')
        f.write('\n'.join(processed_entries))
    
    print(f"\n✅ 处理完成！已保存到: {output_file}")


def main():
    print("=" * 60)
    print("📋 论文自动分类工具")
    print("=" * 60)
    print()
    
    input_file = "new_publications.bib"
    output_file = "classified_publications.bib"
    
    try:
        process_bibtex_file(input_file, output_file)
        
        print("\n" + "=" * 60)
        print("📝 接下来的步骤:")
        print("  1. 查看 classified_publications.bib")
        print("  2. 根据需要微调 keywords")
        print("  3. 准备对应的预览图片")
        print("  4. 添加 PDF 链接、代码链接等")
        print("  5. 将内容合并到 _bibliography/papers.bib")
        print("=" * 60)
        
    except FileNotFoundError:
        print(f"❌ 找不到文件: {input_file}")
        print("请先运行 fetch_publications.py 生成论文列表")
    except Exception as e:
        print(f"❌ 处理出错: {e}")


if __name__ == "__main__":
    main()

