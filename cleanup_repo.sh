#!/bin/bash
# Repository cleanup script
# This removes the virtual environment from git tracking

echo "🧹 Cleaning up repository..."
echo ""

# Remove virtual environment from git
echo "Removing online/ folder from git..."
git rm -r --cached online/ 2>/dev/null || echo "online/ already removed or not tracked"

# Remove pycache
echo "Removing __pycache__/ folders from git..."
git rm -r --cached __pycache__/ 2>/dev/null || echo "__pycache__/ already removed or not tracked"

# Stage .gitignore and packages.txt
echo "Staging updated files..."
git add .gitignore packages.txt

# Show status
echo ""
echo "📊 Current status:"
git status --short

echo ""
echo "✅ Ready to commit! Run:"
echo "   git commit -m 'Clean up: remove virtual environment from git'"
echo "   git push origin main"
