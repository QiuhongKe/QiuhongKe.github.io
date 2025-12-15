# 个人学术网站修改指南

> 本指南详细说明如何修改和定制您的 Jekyll 学术网站的各个部分

---

## 目录

- [1. 首页 (About Page) - 个人简介](#1-首页-about-page---个人简介)
- [2. News (新闻动态)](#2-news-新闻动态)
- [3. Selected Publications (精选论文)](#3-selected-publications-精选论文)
- [4. Publications Page (完整论文列表)](#4-publications-page-完整论文列表)
- [5. Education (教育背景)](#5-education-教育背景)
- [6. Research (研究方向)](#6-research-研究方向)
- [7. Teaching Page (教学经历)](#7-teaching-page-教学经历)
- [8. 导航栏菜单控制](#8-导航栏菜单控制)
- [9. 基本信息配置](#9-基本信息配置)
- [10. 常用操作速查表](#10-常用操作速查表)

---

## 1. 首页 (About Page) - 个人简介

### 📁 文件位置
`_pages/about.md`

### ✏️ 可修改内容

#### 1.1 个人照片
```yaml
---
profile:
  image: prof_pic.jpg  # 修改这里
---
```
- 将您的照片放在 `assets/img/` 目录下
- 推荐尺寸：正方形，至少 400x400 像素
- 支持格式：`.jpg`, `.png`, `.webp`

#### 1.2 显示/隐藏模块
```yaml
---
news: true              # 是否显示 News 板块
selected_papers: true   # 是否显示精选论文
social: true            # 是否显示社交图标
---
```
将 `true` 改为 `false` 可隐藏对应板块

#### 1.3 修改个人简介文字
在 Front Matter 之后的正文部分直接编辑：
```markdown
I am a second-year M.Sc. student...  # 修改这些段落

My research interests include...     # 添加您的内容
```

---

## 2. News (新闻动态)

### 2.1 添加新的 News

在 `_news/` 目录下创建新文件，例如 `announcement_10.md`：

```markdown
---
layout: post
date: 2024-12-11 10:00:00-0400
inline: true
related_posts: false
---

您的新消息内容! [[链接](/path/to/link)]
```

**文件命名建议**：`announcement_N.md` 或 `YYYY-MM-DD-title.md`

### 2.2 删除 News

直接删除 `_news/` 目录下对应的 `.md` 文件即可

### 2.3 控制显示数量和样式

在 `_config.yml` 中找到 `announcements` 配置：

```yaml
announcements:
  enabled: true          # 是否启用 News 功能
  scrollable: true       # 是否可滚动
  limit: 5               # 最多显示 5 条，修改这个数字
  newest_first: true     # true 表示最新的在前
```

### 2.4 完全隐藏 News

在 `_pages/about.md` 中：
```yaml
news: false  # 在首页隐藏
```

---

## 3. Selected Publications (精选论文)

### 3.1 显示/隐藏精选论文

在 `_pages/about.md` 中：
```yaml
selected_papers: true  # 改为 false 可隐藏
```

### 3.2 标记论文为"精选"

在 `_bibliography/papers.bib` 文件中，给想要显示的论文添加：

```bibtex
@article{your_paper,
  title = {Your Paper Title},
  author = {Your Name and Others},
  journal = {Conference Name},
  year = {2024},
  selected = {true},  # 添加这一行标记为精选
}
```

### 3.3 取消精选

将 `selected={true}` 改为 `selected={false}` 或删除这一行

---

## 4. Publications Page (完整论文列表)

### 📁 文件位置
- 论文列表页面：`_pages/publications.md`
- 论文数据：`_bibliography/papers.bib`

### 4.1 添加新论文

在 `_bibliography/papers.bib` 中添加完整的 BibTeX 条目：

```bibtex
@article{tan2025newpaper,
  title = {Your Paper Title},
  author = {Xiaofeng Tan and Coauthor1 and Coauthor2},
  journal = {Conference/Journal Name},
  year = {2025},
  
  % 可选字段
  abbr = {CVPR},                                    # 会议/期刊简称
  ccf = {CCF-A},                                    # CCF 等级标签
  website = {https://your-project-page.com},        # 项目主页
  pdf = {https://arxiv.org/abs/xxxx},               # PDF 链接
  code = {https://github.com/your-repo},            # 代码链接
  selected = {true},                                # 是否在首页显示
  preview = {image-name.png},                       # 预览图（放在 assets/img/publication_preview/）
  abstract = {Your abstract text here...},          # 摘要
  bibtex_show = {true},                             # 显示 BibTeX 按钮
}
```

### 4.2 删除论文

从 `_bibliography/papers.bib` 中删除对应的完整 BibTeX 条目

### 4.3 论文预览图

- 将预览图放在 `assets/img/publication_preview/` 目录
- 推荐尺寸：宽高比 16:9 或 4:3
- 格式：`.png`, `.jpg`, `.webp`

---

## 5. Education (教育背景)

### 方法 1：在首页显示

修改 `_pages/about.md` 的正文部分：

```markdown
## Education

**Southeast University** (2023 - 2025)
- M.Sc. in Computer Science
- Advisor: Prof. XXX

**Shenzhen University** (2019 - 2023)
- B.E. in Computer Science
- B.Sc. in Mathematics (Double Degree)
```

### 方法 2：创建独立页面

在 `_pages/` 目录下创建 `education.md`：

```markdown
---
layout: page
permalink: /education/
title: Education
description: My educational background
nav: true
nav_order: 3
---

## Education

### Southeast University (2023 - 2025)
- **Degree**: M.Sc. in Computer Science
- **Advisor**: Prof. XXX
- **GPA**: X.XX/4.0

### Shenzhen University (2019 - 2023)
- **Degree**: B.E. in Computer Science, B.Sc. in Mathematics
- **GPA**: X.XX/4.0
- **Awards**: XXX Scholarship, XXX Award
```

---

## 6. Research (研究方向)

### 方法 1：在首页显示

修改 `_pages/about.md`：

```markdown
## Research Interests

My research focuses on:
- **RLHF and Reinforcement Learning**: Aligning AI systems with human preferences
- **3D Human Motion Generation**: Creating realistic human animations
- **Diffusion Models**: Generative models for complex data
```

### 方法 2：创建独立研究页面

在 `_pages/` 下创建 `research.md`：

```markdown
---
layout: page
permalink: /research/
title: Research
description: My research interests and projects
nav: true
nav_order: 2
---

## Research Areas

### 1. Motion Generation
Description of your research in this area...

**Key Publications:**
- Paper 1
- Paper 2

### 2. RLHF and Reinforcement Learning
Description...

### 3. Diffusion Models
Description...
```

---

## 7. Teaching Page (教学经历)

### 📁 文件位置
`_pages/teaching.md`

### 扩展示例

```markdown
---
layout: page
permalink: /teaching/
title: Teaching
description: Courses I have taught or TA'd
nav: true
nav_order: 5
---

## Teaching Experience

### Teaching Assistant

#### 2024 Fall - Machine Learning (CS101)
- **University**: Southeast University
- **Instructor**: Prof. XXX
- **Responsibilities**: 
  - Held weekly office hours
  - Graded assignments and exams
  - Prepared tutorial materials

#### 2023 Spring - Data Structures (CS102)
- **University**: Southeast University
- **Instructor**: Prof. YYY
- **Responsibilities**: Lab sessions and homework grading

---

## Guest Lectures

- **Topic**: Introduction to Deep Learning
- **Course**: AI Fundamentals
- **Date**: March 2024
```

---

## 8. 导航栏菜单控制

### 8.1 显示/隐藏页面

在每个页面的 Front Matter 中控制：

```yaml
---
layout: page
title: Page Title
permalink: /page-url/
nav: true        # true 显示在导航栏，false 隐藏
nav_order: 2     # 数字越小越靠前
---
```

### 8.2 调整菜单顺序

修改各页面的 `nav_order` 值：

| 页面 | 文件 | 建议顺序 |
|------|------|----------|
| About | `_pages/about.md` | `nav_order: 1` |
| Research | `_pages/research.md` | `nav_order: 2` |
| Publications | `_pages/publications.md` | `nav_order: 3` |
| Teaching | `_pages/teaching.md` | `nav_order: 4` |
| Projects | `_pages/projects.md` | `nav_order: 5` |

### 8.3 添加新页面到导航栏

在 `_pages/` 目录创建新文件：

```markdown
---
layout: page
permalink: /newpage/
title: New Page
description: Description of the new page
nav: true
nav_order: 6
---

# Your content here
```

---

## 9. 基本信息配置

### 📁 文件位置
`_config.yml` (文件开头部分)

### 9.1 个人基本信息

```yaml
# Site settings
title: blank                        # 网站标题
first_name: Xiaofeng                # 名
middle_name:                        # 中间名（可选）
last_name: Tan                      # 姓
Chinese_name: 谭晓锋                # 中文名
email: xiaofengtan@seu.edu.cn       # 邮箱
description: Personal academic website  # 网站描述
```

### 9.2 社交账号链接

```yaml
# Social accounts
github_username: Xiaofeng-Tan              # GitHub 用户名
twitter_username:                          # Twitter 用户名
linkedin_username: your-linkedin           # LinkedIn 用户名
scholar_userid: C2F5mtgAAAAJ               # Google Scholar ID
orcid_id: 0000-0000-0000-0000              # ORCID ID
```

### 9.3 网站 URL 设置

```yaml
url: https://yourusername.github.io   # 网站 URL
baseurl:                              # 子路径（通常为空）
```

---

## 10. 常用操作速查表

| 操作 | 文件位置 | 具体方法 |
|------|----------|----------|
| 修改个人信息 | `_config.yml` 开头 | 直接编辑基本信息字段 |
| 修改首页介绍 | `_pages/about.md` | 编辑正文内容 |
| 更换头像 | `assets/img/` | 替换图片，修改 `about.md` 中的 `image` 字段 |
| 添加 News | `_news/` 目录 | 新建 `.md` 文件 |
| 删除 News | `_news/` 目录 | 删除对应的 `.md` 文件 |
| 控制 News 数量 | `_config.yml` | 修改 `announcements.limit` |
| 添加论文 | `_bibliography/papers.bib` | 添加 BibTeX 条目 |
| 论文设为精选 | `papers.bib` | 添加 `selected={true}` |
| 隐藏 News | `_pages/about.md` | 设置 `news: false` |
| 隐藏精选论文 | `_pages/about.md` | 设置 `selected_papers: false` |
| 添加新页面 | `_pages/` 目录 | 创建新 `.md` 文件 |
| 调整菜单顺序 | 各页面 Front Matter | 修改 `nav_order` 值 |
| 隐藏页面 | 页面 Front Matter | 设置 `nav: false` |

---

## 快速测试流程

1. **修改文件**：按照上述指南修改对应文件
2. **保存更改**：保存文件后，Jekyll 会自动重新构建（livereload 功能）
3. **查看效果**：刷新浏览器 `http://localhost:4000` 查看效果
4. **调试问题**：如果出现错误，查看终端输出的错误信息

---

## 📂 重要目录结构

```
QiuhongKe.github.io/
├── _config.yml              # 网站主配置文件
├── _pages/                  # 所有页面文件
│   ├── about.md            # 首页
│   ├── publications.md     # 论文列表页
│   ├── teaching.md         # 教学页面
│   └── ...
├── _news/                   # 新闻动态文件
│   ├── announcement_1.md
│   └── ...
├── _bibliography/           # 论文数据
│   └── papers.bib          # BibTeX 格式论文列表
├── assets/
│   ├── img/                # 图片资源
│   │   ├── prof_pic.jpg    # 个人照片
│   │   └── publication_preview/  # 论文预览图
│   └── ...
└── _data/                   # 其他数据文件
    ├── cv.yml              # 简历数据
    └── repositories.yml    # 仓库数据
```

---

## 注意事项

1. **修改后需要重启服务器**：如果修改了 `_config.yml`，需要停止并重新启动 Jekyll 服务器
2. **BibTeX 格式**：确保 `papers.bib` 中的条目格式正确，避免构建错误
3. **图片路径**：图片路径要使用相对于网站根目录的路径
4. **特殊字符**：在 YAML Front Matter 中，如果包含特殊字符（如冒号），需要用引号包裹
5. **备份**：修改前建议备份重要文件

---

## 相关资源

- [Jekyll 官方文档](https://jekyllrb.com/docs/)
- [Liquid 模板语言](https://shopify.github.io/liquid/)
- [Markdown 语法](https://www.markdownguide.org/)
- [BibTeX 格式指南](http://www.bibtex.org/Format/)

---

## 获取帮助

如有问题：
1. 查看终端错误信息
2. 检查文件格式是否正确
3. 确认文件路径是否正确
4. 参考项目现有文件的格式

---

*最后更新：2024年12月11日*
