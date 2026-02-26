# 🧹 Repository Cleanup Instructions

## Problem
Your virtual environment folder (`online/`) with 11,000+ files was committed to GitHub. This is causing:
- Slow deployments on Streamlit Cloud
- Large repository size
- Unnecessary file transfers

## Solution

Run these commands to remove the virtual environment from git:

```bash
# Remove the online folder from git tracking (but keep it locally)
git rm -r --cached online/

# Remove __pycache__ folders too
git rm -r --cached __pycache__/

# Commit the removal
git add .gitignore
git commit -m "Remove virtual environment and cache files from git"

# Push to GitHub
git push origin main
```

## Verify Cleanup

After pushing, check your GitHub repository:
- The `online/` folder should be gone
- Only these files should remain:
  - `app.py`
  - `config.py`
  - `requirements.txt`
  - `Online_curation.csv`
  - `.streamlit/config.toml`
  - `.gitignore`
  - `packages.txt` (empty)
  - Documentation files (*.md)

## After Cleanup

1. **Streamlit Cloud will automatically redeploy** when you push
2. **Deployment will be much faster** (seconds instead of minutes)
3. **The app will work the same** - Streamlit Cloud installs dependencies from `requirements.txt`

## If You Get Errors

If git says files are already deleted:
```bash
# Just commit what's changed
git add .
git commit -m "Clean up repository"
git push origin main
```

## Prevent Future Issues

The `.gitignore` file is already configured to prevent this. Just remember:
- Never commit virtual environment folders
- Always use `.gitignore` before first commit
- Keep only source code and data files in git
