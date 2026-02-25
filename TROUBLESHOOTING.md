# 🔧 Troubleshooting Guide

Common issues and solutions for the Course Explorer application.

---

## TypeError: 'float' object is not subscriptable

### Symptoms
- Application crashes when loading courses
- Error message: `TypeError: 'float' object is not subscriptable`
- Error occurs at line with string slicing (e.g., `[:1200]`)

### Cause
CSV data contains NaN or float values in fields expected to be strings.

### Solution
✅ **Fixed in v2.0.1** - The application now automatically converts all fields to strings and handles NaN values gracefully.

### If Issue Persists
1. Update to latest version
2. Check your CSV file for data quality issues
3. Ensure all text fields contain valid data or are empty (not numeric)

---

## No Courses Displayed

### Symptoms
- Application loads but shows "No courses match your filters"
- Filters appear to be working but no results

### Possible Causes
1. **Too many filters applied**: Combination is too restrictive
2. **Data file missing**: `Online_curation.csv` not found
3. **Data file empty**: CSV has no valid course entries

### Solutions

**1. Clear All Filters**
- Click the "🔄 Clear All Filters" button in the sidebar
- Try searching again with fewer filters

**2. Check Data File**
```bash
# Verify file exists
dir Online_curation.csv  # Windows
ls Online_curation.csv   # Mac/Linux

# Check file size (should be > 0 bytes)
```

**3. Verify CSV Format**
- Open CSV in Excel/text editor
- Ensure it has the required columns
- Check for at least one course with a title

---

## Filters Not Working

### Symptoms
- Selecting filters doesn't change results
- Filter selections don't persist

### Solutions

**1. Refresh the Page**
```
Press Ctrl+R (Windows) or Cmd+R (Mac)
```

**2. Clear Browser Cache**
- Close all Streamlit tabs
- Clear browser cache
- Restart the application

**3. Check Terminal for Errors**
- Look for error messages in the terminal where you ran `streamlit run app.py`
- Address any Python errors shown

---

## Slow Performance

### Symptoms
- Application takes long to load
- Filters are slow to apply
- Cards take time to render

### Solutions

**1. Reduce Dataset Size**
- If you have thousands of courses, consider pagination
- Filter data before loading

**2. Close Other Applications**
- Free up system memory
- Close unnecessary browser tabs

**3. Optimize Data Loading**
```python
# In app.py, adjust cache TTL
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data(path: str = "Online_curation.csv"):
    ...
```

**4. Use List View**
- Switch from Grid to List view for faster rendering
- Grid view renders more HTML elements

---

## Export Not Working

### Symptoms
- Export button doesn't download file
- Downloaded CSV is empty or corrupted

### Solutions

**1. Check Browser Settings**
- Ensure downloads are allowed
- Check download folder permissions

**2. Verify Filtered Data**
- Make sure you have courses showing before exporting
- Clear filters if no results

**3. Try Different Browser**
- Test in Chrome, Firefox, or Edge
- Some browsers handle downloads differently

---

## Search Not Finding Courses

### Symptoms
- Search returns no results for known course titles
- Search seems to be case-sensitive

### Solutions

**1. Check Spelling**
- Verify course title spelling
- Try partial words (e.g., "Pyth" instead of "Python")

**2. Clear Search and Try Again**
- Click the 🗑️ button next to search
- Try different keywords

**3. Search is Case-Insensitive**
- The search should work regardless of case
- If not, report as a bug

---

## Cards Not Displaying Properly

### Symptoms
- Cards overlap or have broken layout
- Badges are cut off
- Text is unreadable

### Solutions

**1. Adjust Browser Zoom**
- Reset zoom to 100% (Ctrl+0 or Cmd+0)
- Try different zoom levels

**2. Resize Browser Window**
- Make window wider for grid view
- Try list view for narrow screens

**3. Clear Browser Cache**
- Force refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

---

## Installation Issues

### Python Not Found

```bash
# Windows
python --version

# Mac/Linux
python3 --version
```

**Solution**: Install Python 3.8+ from [python.org](https://python.org)

### Streamlit Not Installing

```bash
# Try upgrading pip first
pip install --upgrade pip

# Then install streamlit
pip install streamlit pandas
```

### Module Not Found Error

```bash
# Install all requirements
pip install -r requirements.txt

# Or install individually
pip install streamlit
pip install pandas
```

---

## Data Issues

### CSV File Encoding Problems

**Symptoms**: Special characters display incorrectly

**Solution**:
```python
# In app.py, specify encoding
raw = pd.read_csv(path, dtype=str, encoding='utf-8')
```

### Missing Columns

**Symptoms**: KeyError for column name

**Solution**: Check that your CSV has all required columns:
- Competency domain
- Resource title
- URL
- Platform / host
- Stated learning outcomes
- Length (mins)
- Indicated level
- Format type
- Skill area
- Student journey stage

### Duplicate Courses

**Symptoms**: Same course appears multiple times

**Solution**: Clean your CSV data:
```python
# Add to load_data() function
df = df.drop_duplicates(subset=['title', 'platform'])
```

---

## Browser Compatibility

### Recommended Browsers
- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Edge (latest)
- ⚠️ Safari (may have minor issues)
- ❌ Internet Explorer (not supported)

### Known Browser Issues

**Safari**:
- Some CSS animations may not work
- Download button may behave differently

**Firefox**:
- May need to allow popups for export

---

## Getting Help

### Before Reporting an Issue

1. ✅ Check this troubleshooting guide
2. ✅ Review QUICK_START.md
3. ✅ Check terminal for error messages
4. ✅ Try in a different browser
5. ✅ Verify data file is correct

### Reporting a Bug

Include:
- Error message (full text)
- Steps to reproduce
- Browser and version
- Python version
- Screenshot (if applicable)

### Useful Commands

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Check Streamlit version
streamlit --version

# Run with debug info
streamlit run app.py --logger.level=debug
```

---

## Performance Tips

### For Large Datasets (1000+ courses)

1. **Enable Pagination**
   - See ENHANCEMENTS_GUIDE.md for implementation

2. **Optimize Filters**
   - Use categorical data types
   - Pre-filter data before loading

3. **Reduce Card Complexity**
   - Limit skill badges shown
   - Shorten descriptions

### For Slow Networks

1. **Minimize External Resources**
   - Host fonts locally
   - Reduce image sizes

2. **Enable Caching**
   - Increase cache TTL
   - Cache more operations

---

## Common Questions

### Q: Can I use Excel files instead of CSV?

**A**: Yes, modify the load function:
```python
df = pd.read_excel(path, dtype=str)
```

### Q: How do I add more courses?

**A**: Add rows to `Online_curation.csv` and refresh the app

### Q: Can I change the color scheme?

**A**: Yes, edit `config.py` or the CSS section in `app.py`

### Q: How do I deploy this online?

**A**: See README.md deployment section or ENHANCEMENTS_GUIDE.md

### Q: Can multiple users access this?

**A**: Yes, deploy to Streamlit Cloud or a web server

---

## Emergency Fixes

### App Won't Start At All

```bash
# 1. Kill any running Streamlit processes
# Windows
taskkill /F /IM streamlit.exe

# Mac/Linux
pkill -f streamlit

# 2. Clear Streamlit cache
streamlit cache clear

# 3. Reinstall dependencies
pip uninstall streamlit pandas
pip install streamlit pandas

# 4. Try running again
streamlit run app.py
```

### Data Completely Broken

```bash
# 1. Backup current CSV
copy Online_curation.csv Online_curation.csv.backup

# 2. Verify CSV structure
# Open in Excel and check columns

# 3. Re-export from source if needed
```

---

**Last Updated**: 2024
**Version**: 2.0.1

For additional help, see:
- README.md
- QUICK_START.md
- ENHANCEMENTS_GUIDE.md
- BUGFIX_NOTES.md
