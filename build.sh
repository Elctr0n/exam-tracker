#!/bin/bash
# Render build script for ExamX Flask app

echo "🚀 Starting ExamX build process..."

# Upgrade pip first
pip install --upgrade pip

# Install Python dependencies with verbose output
echo "📦 Installing dependencies..."
pip install -r requirements.txt --no-cache-dir

echo "✅ Dependencies installed successfully"
echo "🔗 Database connection will be established at runtime"
echo "🎯 ExamX app ready for deployment!"
