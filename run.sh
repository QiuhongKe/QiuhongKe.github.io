#!/bin/bash

# Jekyll Academic Website Quick Start Script
# Author: Qiuhong Ke
# Purpose: Quick start Jekyll development server

echo "🚀 Starting Jekyll Academic Website..."
echo "================================"

# Check if dependencies need to be installed
if [ ! -d "vendor/bundle" ] && [ ! -f "Gemfile.lock" ]; then
    echo "📦 First run, installing dependencies..."
    bundle install
elif [ "$1" == "--install" ] || [ "$1" == "-i" ]; then
    echo "📦 Reinstalling dependencies..."
    bundle install
fi

# Start server
echo "🌐 Starting server at http://localhost:4000"
echo "💡 Press Ctrl+C to stop the server"
echo "================================"

# Start Jekyll server
# --livereload: Auto-refresh browser
# --open-url: Auto-open browser (optional)
# Use arch -x86_64 to run via Rosetta 2 for Apple Silicon compatibility
if [ "$1" == "--open" ] || [ "$2" == "--open" ]; then
    arch -x86_64 /bin/zsh -c "export BUNDLE_PATH=vendor/bundle && bundle exec jekyll serve --livereload --open-url"
else
    arch -x86_64 /bin/zsh -c "export BUNDLE_PATH=vendor/bundle && bundle exec jekyll serve --livereload"
fi
