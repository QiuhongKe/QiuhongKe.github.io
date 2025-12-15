#!/bin/bash

# Jekyll网站依赖自动安装脚本
# 适用于Apple Silicon Mac

set -e

echo "======================================"
echo "Jekyll网站依赖安装脚本"
echo "======================================"
echo ""

# 检查是否是Apple Silicon
ARCH=$(uname -m)
if [ "$ARCH" != "arm64" ]; then
    echo "⚠️  警告：您的系统不是arm64架构，此脚本主要为Apple Silicon Mac设计"
    echo "当前架构：$ARCH"
    read -p "是否继续？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 检查Homebrew
echo "🔍 检查Homebrew..."
if ! command -v brew &> /dev/null; then
    echo "📦 Homebrew未安装，正在安装..."
    echo "这可能需要几分钟，并且可能需要您输入密码。"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # 添加Homebrew到PATH
    if [ -f /opt/homebrew/bin/brew ]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
else
    echo "✅ Homebrew已安装"
fi

# 检查Ruby
echo ""
echo "🔍 检查Ruby..."
RUBY_PATH=$(which ruby)
if [[ "$RUBY_PATH" == "/usr/bin/ruby" ]]; then
    echo "⚠️  当前使用系统Ruby，需要安装Homebrew版本"
    echo "📦 正在安装Ruby..."
    brew install ruby
    
    # 添加Ruby到PATH
    echo ""
    echo "📝 配置Ruby环境变量..."
    RUBY_CONFIG='export PATH="/opt/homebrew/opt/ruby/bin:$PATH"'
    RUBY_CONFIG2='export PATH="/opt/homebrew/lib/ruby/gems/3.3.0/bin:$PATH"'
    
    if ! grep -q "/opt/homebrew/opt/ruby/bin" ~/.zshrc 2>/dev/null; then
        echo "$RUBY_CONFIG" >> ~/.zshrc
        echo "$RUBY_CONFIG2" >> ~/.zshrc
    fi
    
    # 立即加载配置
    export PATH="/opt/homebrew/opt/ruby/bin:$PATH"
    export PATH="/opt/homebrew/lib/ruby/gems/3.3.0/bin:$PATH"
else
    echo "✅ 已安装非系统Ruby: $RUBY_PATH"
fi

# 显示Ruby版本
echo ""
echo "📊 Ruby版本信息："
/opt/homebrew/opt/ruby/bin/ruby -v 2>/dev/null || ruby -v
echo "平台: $(ruby -e 'puts RUBY_PLATFORM')"

# 安装Bundler
echo ""
echo "🔍 检查Bundler..."
if ! command -v bundle &> /dev/null; then
    echo "📦 正在安装Bundler..."
    gem install bundler
else
    echo "✅ Bundler已安装"
fi

# 安装Jekyll依赖
echo ""
echo "📦 安装Jekyll和项目依赖..."
cd "$(dirname "$0")"
rm -rf vendor/bundle Gemfile.lock .bundle

echo "正在安装gems，这可能需要几分钟..."
bundle install --path vendor/bundle

echo ""
echo "======================================"
echo "✅ 安装完成！"
echo "======================================"
echo ""
echo "现在您可以运行以下命令启动网站："
echo "  bash run.sh"
echo ""
echo "或者使用以下命令在新终端中："
echo "  source ~/.zshrc"
echo "  cd $(pwd)"
echo "  bash run.sh"
echo ""

