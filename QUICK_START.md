# 🚀 Quick Start Guide

Get your Course Explorer up and running in 5 minutes!

## Prerequisites

- Python 3.8 or higher installed
- Basic command line knowledge

## Installation Steps

### 1. Install Python Dependencies

Open your terminal/command prompt and run:

```bash
pip install streamlit pandas
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### 2. Verify Your Data File

Make sure `Online_curation.csv` is in the same folder as `app.py`.

Your folder structure should look like:
```
your-project-folder/
├── app.py
├── Online_curation.csv
├── config.py
├── requirements.txt
└── README.md
```

### 3. Run the Application

In your terminal, navigate to the project folder and run:

```bash
streamlit run app.py
```

### 4. Open in Browser

The app will automatically open in your default browser at:
```
http://localhost:8501
```

If it doesn't open automatically, copy the URL from the terminal and paste it into your browser.

## Using the Application

### Basic Navigation

1. **Search Bar** (Left Sidebar)
   - Type keywords to search course titles and descriptions
   - Example: "Python", "statistics", "machine learning"

2. **Filters** (Left Sidebar)
   - Select multiple options from each filter
   - Filters work together (AND logic)
   - Use "Clear All Filters" button to reset

3. **View Options** (Top Bar)
   - **Grid View**: See 3 courses per row with cards
   - **List View**: See 1 course per row for detailed scanning

4. **Sorting** (Top Bar)
   - Sort by duration, title, or relevance
   - Helps find shortest/longest courses quickly

5. **Export** (Top Bar)
   - Download filtered results as CSV
   - Opens in Excel or Google Sheets

### Exploring Courses

Each course card shows:
- **Title**: Course name
- **Badges**: Domain, level, format, journey stage
- **Platform**: Where the course is hosted
- **Duration**: Estimated time to complete
- **Skills**: Key skills you'll learn
- **Description**: Brief overview

### Getting More Details

Click on a course card to expand:

1. **📖 Preview**
   - Full course description
   - Learning outcomes
   - Prerequisites
   - Direct link to course

2. **📋 Quick Assign**
   - Pre-formatted recommendation text
   - Copy and paste into email or LMS
   - Includes all key details

## Tips & Tricks

### Finding the Right Course

1. **Start Broad**: Use domain filters first
2. **Narrow Down**: Add skill or level filters
3. **Check Duration**: Use the slider to match available time
4. **Sort Smart**: Sort by duration to find quick wins

### For Teaching Assistants

1. **Create Recommendations**:
   - Filter by student's skill level
   - Check prerequisites match student background
   - Use "Quick Assign" to generate recommendation

2. **Track Popular Courses**:
   - Check the stats dashboard
   - Note most common platforms
   - See average durations

3. **Export Lists**:
   - Create custom course lists for different student groups
   - Export and share via email
   - Import into your LMS

### For Students

1. **Plan Your Learning Path**:
   - Filter by "Student Journey Stage"
   - Start with "Pre-arrival" courses
   - Progress through "Ongoing study"

2. **Match Your Level**:
   - Use level filter (Beginner/Intermediate/Advanced)
   - Check prerequisites before enrolling
   - Look for courses that build on each other

3. **Time Management**:
   - Use duration filter to find courses that fit your schedule
   - Sort by duration to see time commitment
   - Mix short and long courses

## Common Issues

### App Won't Start

**Problem**: `streamlit: command not found`

**Solution**: 
```bash
pip install --upgrade streamlit
```

### Data Not Loading

**Problem**: "File not found" error

**Solution**: 
- Check that `Online_curation.csv` is in the same folder as `app.py`
- Check the filename spelling (case-sensitive on Mac/Linux)

### Filters Not Working

**Problem**: No results after applying filters

**Solution**:
- Click "Clear All Filters" and try again
- Check if your filter combination is too restrictive
- Try removing filters one by one

### Slow Performance

**Problem**: App is slow with many courses

**Solution**:
- Close other browser tabs
- Refresh the page (Ctrl+R or Cmd+R)
- Clear browser cache
- Restart the Streamlit server

## Keyboard Shortcuts

- **Ctrl/Cmd + R**: Refresh the app
- **Ctrl/Cmd + F**: Search in page
- **Tab**: Navigate between filters
- **Enter**: Apply filter selection

## Next Steps

Once you're comfortable with the basics:

1. **Customize the UI**: Edit `config.py` to change colors and settings
2. **Add Features**: Check `ENHANCEMENTS_GUIDE.md` for ideas
3. **Share with Team**: Deploy to Streamlit Cloud (see README.md)

## Getting Help

- **Documentation**: See `README.md` for detailed information
- **Enhancements**: See `ENHANCEMENTS_GUIDE.md` for customization
- **Issues**: Check the terminal for error messages

## Video Tutorial

*(Coming soon - placeholder for video walkthrough)*

---

**Ready to explore?** Run `streamlit run app.py` and start discovering courses! 🎓
