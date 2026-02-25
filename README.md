# 🎓 Course Explorer — Student Success

A modern, scalable Streamlit application for showcasing curated courses from an Excel/CSV dataset. Built for TA-assisted advising and student success support.

## ✨ Features

### Core Functionality
- **Smart Search**: Full-text search across course titles and descriptions
- **Advanced Filtering**: Multi-select filters for domains, skills, levels, formats, platforms, and journey stages
- **Duration Filtering**: Slider-based duration range selection
- **Sorting Options**: Sort by relevance, duration, or title
- **View Modes**: Toggle between grid and list views
- **Export Functionality**: Download filtered results as CSV

### UI/UX Enhancements
- **Modern Dark Theme**: Premium gradient cards with smooth hover effects
- **Responsive Design**: Mobile-friendly layout that adapts to screen size
- **Visual Hierarchy**: Clear information architecture with badges and color coding
- **Interactive Stats Dashboard**: Real-time statistics about the course catalog
- **Quick Insights**: Average duration and most common attributes for filtered results
- **Clear All Filters**: One-click filter reset

### Course Cards
Each course card displays:
- Course title and description
- Domain, level, format, and journey stage badges
- Platform and duration information
- Priority skills tags
- Preview with full details (learning outcomes, prerequisites)
- Quick assign feature for TA recommendations
- Direct link to course (when available)

## 🚀 Getting Started

### Prerequisites
```bash
Python 3.8+
pip install streamlit pandas
```

### Installation
1. Clone or download this repository
2. Ensure `Online_curation.csv` is in the same directory as `app.py`
3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📊 Data Structure

The application expects a CSV file with the following columns:
- `Competency domain`: Subject area
- `Focus Areas`: Specific focus within domain
- `Resource title`: Course name
- `URL`: Link to course
- `Platform / host`: Course provider
- `Resource type`: Type of resource
- `Stated learning outcomes`: Course description
- `Stated prerequisites`: Required knowledge
- `Length (mins)`: Duration (flexible format)
- `Indicated level`: Beginner/Intermediate/Advanced
- `Format type`: Interactive/Passive
- `Skill area`: Priority skills covered
- `Student journey stage`: When to take the course
- Additional metadata columns

## 🎨 Customization

### Adding New Filters
To add a new filter, edit the sidebar section in `app.py`:
```python
new_filter = st.multiselect("New Filter", df["column_name"].unique())
```

Then add the filter logic:
```python
if new_filter:
    mask &= df["column_name"].isin(new_filter)
```

### Changing Colors
Modify the CSS section at the top of `app.py`. Key color variables:
- Background: `#0f1117`
- Card background: `#1e293b` to `#0f172a`
- Accent gradient: `#6ee7b7` to `#3b82f6`
- Border: `#334155`

### Adjusting Grid Layout
Change the `COLS` variable in the card grid section:
```python
COLS = 3  # Change to 2 or 4 for different layouts
```

## 📈 Scalability

The application is designed to scale:
- **Data Caching**: Uses `@st.cache_data` for efficient data loading
- **Flexible Parsing**: Handles various duration formats automatically
- **Dynamic Filters**: Automatically adapts to data changes
- **Efficient Filtering**: Uses pandas boolean indexing for fast filtering
- **Modular Structure**: Easy to extend with new features

## 🔧 Technical Details

### Duration Parsing
The app intelligently parses various duration formats:
- "16 hours"
- "5 hours a day for 3 days"
- "12 weeks" (estimated at 5 hrs/week)
- "One semester" (estimated at 45 hours)
- "35 videos roughly 50 mins each"

### Performance Optimizations
- Data loaded once and cached
- Efficient pandas operations for filtering
- Minimal re-renders with proper state management
- Lazy loading of course details in expanders

## 🎯 Use Cases

1. **Student Advising**: TAs can quickly find relevant courses for students
2. **Course Discovery**: Students can explore courses by skill or domain
3. **Curriculum Planning**: Identify gaps in course offerings
4. **Resource Management**: Track course catalog statistics
5. **Export & Share**: Download filtered course lists for offline use

## 🛠️ Future Enhancements

Potential improvements:
- User authentication and saved filters
- Course recommendations based on student profile
- Integration with LMS systems
- Course completion tracking
- Rating and review system
- Advanced analytics dashboard
- Multi-language support

## 📝 License

This project is for educational purposes as part of CMU Student Success Support.

## 🤝 Contributing

To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📧 Support

For questions or issues, contact the Student Success team.

---

Built with ❤️ using Streamlit
