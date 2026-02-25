# 🚀 Enhancement Guide for Course Explorer

This guide provides detailed instructions for common enhancements and customizations to the Course Explorer application.

## Table of Contents
1. [Adding New Filters](#adding-new-filters)
2. [Customizing the UI](#customizing-the-ui)
3. [Adding New Features](#adding-new-features)
4. [Performance Optimization](#performance-optimization)
5. [Data Integration](#data-integration)

---

## Adding New Filters

### Step 1: Add Filter UI in Sidebar
In `app.py`, locate the sidebar section and add your new filter:

```python
# Example: Adding a "Cost" filter
costs = sorted({c for c in df["cost"].unique() if c})
sel_costs = st.multiselect("Cost Range", costs, help="Filter by course cost")
```

### Step 2: Apply Filter Logic
In the filtering logic section, add the condition:

```python
if sel_costs:
    mask &= df["cost"].isin(sel_costs)
```

### Step 3: Update Config (Optional)
Add the filter to `config.py`:

```python
ENABLED_FILTERS = [
    "search",
    "domain",
    "skills",
    "cost",  # New filter
    # ... other filters
]
```

---

## Customizing the UI

### Changing Colors

#### Method 1: Edit CSS Directly
Locate the CSS section in `app.py` and modify color values:

```css
/* Change primary gradient */
background: linear-gradient(90deg, #YOUR_COLOR_1, #YOUR_COLOR_2);

/* Change card background */
.course-card {
    background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
}
```

#### Method 2: Use Config File
Update `config.py` with your color scheme:

```python
DOMAIN_COLORS = [
    "#FF6B6B",  # Red
    "#4ECDC4",  # Teal
    "#45B7D1",  # Blue
    # Add more colors
]
```

### Changing Layout

#### Grid Columns
Modify the number of columns in grid view:

```python
# In app.py, find:
if view_mode == "Grid":
    COLS = 3  # Change to 2, 4, or any number
```

#### Card Size
Adjust card padding and sizing in CSS:

```css
.course-card {
    padding: 1.5rem 2rem 1.25rem;  /* Increase for larger cards */
    min-height: 300px;  /* Set minimum height */
}
```

### Adding Custom Badges

1. Define badge style in CSS:
```css
.badge-custom {
    background: #YOUR_COLOR;
    color: #TEXT_COLOR;
}
```

2. Add badge to card rendering:
```python
if custom_field:
    badges += f'<span class="badge badge-custom">{custom_field}</span>'
```

---

## Adding New Features

### Feature 1: Course Comparison

```python
# Add to sidebar
st.markdown("### 📊 Compare Courses")
compare_courses = st.multiselect(
    "Select courses to compare",
    filtered["title"].tolist(),
    max_selections=3
)

if compare_courses:
    comparison_df = filtered[filtered["title"].isin(compare_courses)]
    st.dataframe(comparison_df[["title", "duration_hours", "level", "platform"]])
```

### Feature 2: Favorites/Bookmarks

```python
# Initialize session state
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# Add favorite button in card
if st.button(f"⭐ Favorite", key=f"fav_{row['id']}"):
    if row['id'] not in st.session_state.favorites:
        st.session_state.favorites.append(row['id'])
        st.success("Added to favorites!")

# Show favorites in sidebar
if st.session_state.favorites:
    st.sidebar.markdown("### ⭐ Your Favorites")
    fav_courses = df[df["id"].isin(st.session_state.favorites)]
    for _, course in fav_courses.iterrows():
        st.sidebar.write(f"- {course['title']}")
```

### Feature 3: Advanced Search with Filters

```python
# Add search options
search_in = st.multiselect(
    "Search in",
    ["Title", "Description", "Skills", "Platform"],
    default=["Title", "Description"]
)

# Modify search logic
if search_q:
    q_low = search_q.lower()
    search_mask = pd.Series(False, index=df.index)
    
    if "Title" in search_in:
        search_mask |= df["title"].str.lower().str.contains(q_low, na=False)
    if "Description" in search_in:
        search_mask |= df["short_description"].str.lower().str.contains(q_low, na=False)
    if "Skills" in search_in:
        search_mask |= df["priority_skills"].str.lower().str.contains(q_low, na=False)
    if "Platform" in search_in:
        search_mask |= df["platform"].str.lower().str.contains(q_low, na=False)
    
    mask &= search_mask
```

### Feature 4: Course Recommendations

```python
def get_recommendations(course_id, df, n=3):
    """Get similar courses based on domain and skills"""
    course = df[df["id"] == course_id].iloc[0]
    
    # Calculate similarity score
    similar = df.copy()
    similar["score"] = 0
    
    # Same domain: +3 points
    similar.loc[similar["domain"] == course["domain"], "score"] += 3
    
    # Same level: +2 points
    similar.loc[similar["level"] == course["level"], "score"] += 2
    
    # Overlapping skills: +1 point per skill
    for _, row in similar.iterrows():
        overlap = set(course["skill_tags"]) & set(row["skill_tags"])
        similar.loc[similar["id"] == row["id"], "score"] += len(overlap)
    
    # Exclude the course itself
    similar = similar[similar["id"] != course_id]
    
    return similar.nlargest(n, "score")

# Use in card preview
with st.expander("🔗 Similar Courses"):
    recommendations = get_recommendations(row["id"], df)
    for _, rec in recommendations.iterrows():
        st.write(f"- {rec['title']} ({rec['domain']})")
```

---

## Performance Optimization

### 1. Optimize Data Loading

```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data(path: str = "Online_curation.csv") -> pd.DataFrame:
    # Use specific dtypes to reduce memory
    dtypes = {
        "title": "string",
        "domain": "category",
        "level": "category",
        "format": "category",
        "platform": "category"
    }
    
    raw = pd.read_csv(path, dtype=dtypes)
    # ... rest of processing
    return df
```

### 2. Lazy Loading for Large Datasets

```python
# Add pagination
ITEMS_PER_PAGE = 12

page = st.number_input("Page", min_value=1, max_value=(len(filtered) // ITEMS_PER_PAGE) + 1, value=1)
start_idx = (page - 1) * ITEMS_PER_PAGE
end_idx = start_idx + ITEMS_PER_PAGE

paginated_data = filtered.iloc[start_idx:end_idx]
```

### 3. Optimize Filtering

```python
# Use categorical data types for frequently filtered columns
df["domain"] = df["domain"].astype("category")
df["level"] = df["level"].astype("category")
df["format"] = df["format"].astype("category")

# This makes filtering much faster for large datasets
```

---

## Data Integration

### Connecting to Google Sheets

```python
import gspread
from google.oauth2.service_account import Credentials

@st.cache_data(ttl=600)  # Cache for 10 minutes
def load_from_sheets(sheet_url):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
    client = gspread.authorize(creds)
    
    sheet = client.open_by_url(sheet_url).sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data)
```

### Connecting to Database

```python
import sqlite3

@st.cache_data
def load_from_db(db_path="courses.db"):
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM courses"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
```

### API Integration

```python
import requests

@st.cache_data(ttl=3600)
def load_from_api(api_url):
    response = requests.get(api_url)
    data = response.json()
    return pd.DataFrame(data)
```

---

## Testing Your Changes

### 1. Run Locally
```bash
streamlit run app.py
```

### 2. Test Different Screen Sizes
- Desktop: Full browser window
- Tablet: Resize browser to ~768px width
- Mobile: Resize browser to ~375px width

### 3. Test Performance
```python
import time

start = time.time()
# Your code here
end = time.time()
print(f"Execution time: {end - start:.2f} seconds")
```

### 4. Check for Errors
Monitor the terminal for any error messages or warnings.

---

## Deployment

### Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy!

### Deploy to Heroku

1. Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT
```

2. Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
```

3. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

---

## Best Practices

1. **Always test changes locally** before deploying
2. **Use version control** (Git) to track changes
3. **Document your changes** in comments
4. **Keep the config file updated** with new settings
5. **Optimize for performance** with large datasets
6. **Make UI responsive** for all screen sizes
7. **Add error handling** for edge cases
8. **Use caching** for expensive operations

---

## Need Help?

- Check Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)
- Pandas documentation: [pandas.pydata.org](https://pandas.pydata.org)
- Community forum: [discuss.streamlit.io](https://discuss.streamlit.io)

---

Happy coding! 🚀
