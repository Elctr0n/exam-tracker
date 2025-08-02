#!/bin/bash
# Render build script for ExamX Flask app

echo "🚀 Starting ExamX build process..."

# Check Python version
echo "🐍 Checking Python version..."
python --version
echo "Expected: Python 3.11.x"

# Upgrade pip first
echo "🔄 Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies with verbose output
echo "📦 Installing dependencies..."
pip install -r requirements.txt --no-cache-dir --verbose

# Verify critical imports
echo "🔍 Verifying critical imports..."
python -c "import flask; print(f'Flask: {flask.__version__}')"
python -c "import psycopg; print(f'psycopg: {psycopg.__version__}')" || python -c "import psycopg2; print(f'psycopg2: {psycopg2.__version__}')"

echo "✅ Dependencies installed successfully"
echo "🔗 Database connection will be established at runtime"
echo "🎯 ExamX app ready for deployment!"
