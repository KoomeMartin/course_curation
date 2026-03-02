# Streamlit Cloud Cache Issue - How to Fix

## Problem
After pushing updated `Online_curation.csv` to GitHub, Streamlit Cloud is still showing old data because of caching.

## Solution Options

### Option 1: Clear Cache from Streamlit Cloud Dashboard (RECOMMENDED)
1. Go to your Streamlit Cloud dashboard: https://share.streamlit.io/
2. Find your app: `coursecuration-xllfuqlg2rcry5xn3dqdsk.streamlit.app`
3. Click the **⋮** (three dots menu) next to your app
4. Select **"Reboot app"** or **"Clear cache"**
5. Wait for the app to restart (usually 30-60 seconds)
6. Refresh your browser

### Option 2: Add Cache TTL (Already Applied)
I've updated `app.py` to include a cache TTL (Time To Live) of 1 hour:
```python
@st.cache_data(show_spinner="Loading course catalogue…", ttl=3600)  # Cache for 1 hour
```

This means the cache will automatically refresh every hour.

### Option 3: Force Cache Refresh with Version Parameter
Add a version parameter to force cache refresh:

```python
# In app.py, add a version constant at the top
DATA_VERSION = "2026-03-02"  # Update this date when data changes

@st.cache_data(show_spinner="Loading course catalogue…")
def load_data(path: str = "Online_curation.csv", version: str = DATA_VERSION) -> pd.DataFrame:
    # ... rest of the function
```

Then call it with:
```python
df = load_data(version=DATA_VERSION)
```

### Option 4: Manual Cache Clear via App
Add a button in the sidebar to clear cache:

```python
with st.sidebar:
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()
```

## Current Status

✅ **Applied**: Cache TTL of 1 hour added to `load_data()` function
✅ **Committed**: Changes pushed to GitHub
⏳ **Pending**: Streamlit Cloud needs to pull latest changes and restart

## Steps to Verify Fix

1. **Check GitHub**: Verify `Online_curation.csv` has 332 rows
   - Go to: https://github.com/[your-username]/course_curation/blob/main/Online_curation.csv
   - Check file size: ~134 KB (was ~86 KB before)

2. **Reboot Streamlit App**:
   - Go to Streamlit Cloud dashboard
   - Reboot the app
   - Wait for restart

3. **Verify in App**:
   - Check "Total Courses" stat card should show **332** (not 262)
   - Check "Platforms" filter should include **LinkedIn Learning**
   - Search for "LinkedIn" in the search bar
   - Should see 59 LinkedIn Learning courses

## Expected Results After Fix

### Stats Dashboard
- Total Courses: **332** (was 262)
- Platforms: Should include "LinkedIn Learning" with 59 courses
- Top Focus Areas: Data Science should show 27 courses (was 17)

### Platform Filter
Should now include:
- CARMA (73)
- LinkedIn Learning (59) ← NEW!
- SAGECampus (58)
- Software Engineering Institute (SEI) (29)
- SASC Communication Support (26)
- OLI (26)

### Search Test
Search for "Model Context Protocol" should return the LinkedIn Learning course.

## Troubleshooting

### If data still not updating after reboot:
1. Check Streamlit Cloud logs for errors
2. Verify GitHub commit is on main branch
3. Check if Streamlit Cloud is pulling from correct branch
4. Try "Reboot app" again (sometimes takes 2 tries)

### If you see errors in logs:
- Check for CSV parsing errors
- Verify file encoding is UTF-8
- Check for any special characters in new data

## Quick Verification Command

Run locally to verify data:
```bash
python -c "import pandas as pd; df = pd.read_csv('Online_curation.csv'); print(f'Total: {len(df)}'); linkedin = df[df['Platform / host'].str.contains('LinkedIn', na=False)]; print(f'LinkedIn: {len(linkedin)}')"
```

Expected output:
```
Total: 332
LinkedIn: 59
```

## Contact Support

If issues persist after trying all options:
1. Check Streamlit Community Forum: https://discuss.streamlit.io/
2. File issue on Streamlit GitHub: https://github.com/streamlit/streamlit/issues
3. Check app logs in Streamlit Cloud dashboard
