# Jekyll网站依赖修复指南

## 问题诊断

您的系统遇到了Ruby架构不匹配的问题。macOS系统自带的Ruby (2.6.10) 在Rosetta模式下运行（x86_64模拟），但您的Mac是Apple Silicon (arm64)架构。这导致某些需要原生扩展的Ruby gems无法正确加载。

##解决方案

### 方案1: 使用Docker（推荐）

这是最简单可靠的方案，完全避免架构兼容性问题。

1. 安装Docker Desktop for Mac (Apple Silicon版本)
   - 访问: https://www.docker.com/products/docker-desktop
   - 下载并安装 Apple Silicon 版本

2. 启动网站：
```bash
docker-compose up
```

网站将在 http://localhost:8080 运行

### 方案2: 安装Homebrew和原生Ruby

1. 安装Homebrew（如果还没有安装）:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. 安装Ruby:
```bash
brew install ruby
```

3. 将Homebrew的Ruby添加到PATH（添加到 ~/.zshrc）:
```bash
echo 'export PATH="/opt/homebrew/opt/ruby/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

4. 重新安装依赖:
```bash
cd /Users/zinuo/Desktop/PhD/qiuhongke
rm -rf vendor/bundle Gemfile.lock .bundle
bundle install --path vendor/bundle
```

5. 运行网站:
```bash
bash run.sh
```

### 方案3: 使用rbenv（供Ruby开发者使用）

如果您经常使用Ruby开发，rbenv可以让您管理多个Ruby版本:

1. 安装rbenv:
```bash
brew install rbenv ruby-build
```

2. 初始化rbenv:
```bash
rbenv init
# 按照提示将初始化命令添加到~/.zshrc
```

3. 安装Ruby 3.2:
```bash
rbenv install 3.2.2
rbenv local 3.2.2
```

4. 安装依赖并运行:
```bash
gem install bundler
bundle install --path vendor/bundle
bash run.sh
```

## 当前状态

- ✅ Gemfile已准备好
- 需要正确的Ruby环境（原生arm64或Docker）
- 系统Ruby (2.6.10) 在Rosetta模式下运行，会导致架构不匹配

## 推荐

对于学术网站用户，**强烈推荐方案1（Docker）**，因为：
- 不需要修改系统配置
- 与团队成员环境一致
- 避免Ruby版本冲突
- 一键启动，简单可靠

