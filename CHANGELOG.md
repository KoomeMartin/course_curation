# 📋 Changelog

All notable changes to the Course Explorer project.

---

## [2.1.1] - 2024 (Current Release)

### ✨ Improved
- **Cleaner Tiles**: Removed skill badges from tiles for a more streamlined appearance
- **Brief Information Only**: Tiles now show only essential course info (title, badges, platform, duration, description)
- **Filtered Skills Display**: Details view now filters out long competency descriptions, showing only concise skill names
- **Better Sidebar Scrolling**: Fixed scrolling conflicts between multiselect dropdowns and sidebar
- **Optimized Content Length**: Reduced text lengths in details view for better scannability

### 🎨 UI/UX
- Removed verbose skill descriptions from tile display
- Skills section in details view now shows only clean, short skill names (< 100 chars)
- Limited skills display to 10 items maximum
- Improved multiselect dropdown scrolling (400px max height)
- Enhanced sidebar scrollability with proper overflow handling
- Compact filter spacing for better density

### 🔧 Technical
- Removed skill_badges generation code for tiles
- Added skill filtering logic (length < 100 characters)
- Enhanced CSS for independent dropdown and sidebar scrolling
- Reduced learning outcomes display from 1200 to 800 characters
- Reduced prerequisites display from 400 to 300 characters

---

## [2.1.0] - 2024

### ✨ Improved
- **Cleaner Card Design**: Removed Quick Assign button for a more streamlined showcase experience
- **Single Action Button**: Each card now has one clear "View Details" button
- **Better Details View**: Enhanced course details display with organized metadata and direct course links
- **Fixed Top Skill Areas**: Resolved text overflow issue with proper flex wrapping
- **Clickable Cards**: Cards now have cursor pointer and clear interaction pattern
- **Less Clutter**: Simplified interface focused on course discovery

### 🎨 UI/UX
- Removed dual-button layout (Preview + Quick Assign)
- Added single "View Details" button per card
- Improved details view with 2-column metadata layout
- Fixed skill badges overflow in stats dashboard
- Enhanced card spacing and breathing room
- Better visual hierarchy

### 🔧 Technical
- Removed unused Quick Assign CSS
- Simplified card rendering logic
- Reduced DOM elements per card by ~40%
- Updated config.py to reflect feature changes

---

## [2.0.1] - 2024

### 🐛 Fixed
- **Critical Bug**: Fixed TypeError when course data contains NaN/float values instead of strings
  - Added type conversion for all string fields before operations
  - Added `isinstance()` checks before string slicing
  - Enhanced `_skill_tags` function to handle non-string types
  - Added safety checks in badge generation
  - Fixed top skills display to handle mixed types
- Improved error handling for missing/null data across all card fields

### 🔧 Technical
- Added comprehensive type safety to prevent subscripting errors
- Enhanced data validation in skill tags parsing
- Improved null value handling throughout the application

---

## [2.0.0] - 2024

### ✨ Added
- **View Toggle**: Switch between Grid (3 columns) and List (1 column) views
- **Sorting System**: 5 sorting options (Relevance, Duration, Title)
- **Export Feature**: Download filtered courses as CSV with date stamp
- **Quick Insights**: Footer analytics showing average duration, most common platform/level
- **Clear All Filters**: One-click button to reset all filters
- **Search Clear Button**: Quick reset for search field
- **Platform Badge**: New badge type for course platforms
- **Help Tooltips**: Contextual help on all filter options
- **Configuration File**: `config.py` for easy customization
- **Comprehensive Documentation**:
  - README.md (project overview)
  - QUICK_START.md (5-minute setup guide)
  - ENHANCEMENTS_GUIDE.md (customization guide)
  - IMPROVEMENTS_SUMMARY.md (detailed changes)
  - CHANGELOG.md (this file)

### 🎨 Improved
- **Header Design**: Gradient card with better visual hierarchy
- **Card Animations**: Smooth hover effects with lift animation
- **Badge Hover Effects**: Interactive badge scaling
- **Stat Cards**: Added hover animations and better transitions
- **Sidebar Organization**: Better grouping with section headers
- **Responsive Design**: Mobile-friendly breakpoints and adaptive sizing
- **Color Scheme**: Enhanced gradient and badge colors
- **Typography**: Better font weights and sizing
- **Spacing**: Improved padding and margins throughout

### 🔧 Technical
- **Code Organization**: Clear section separators and improved comments
- **Performance**: Optimized pandas operations and filtering logic
- **Caching**: Better use of `@st.cache_data` decorator
- **Error Handling**: Graceful handling of missing/null data
- **Modular CSS**: Better organized styles with clear sections
- **Type Hints**: Added datetime import for export functionality

### 🐛 Fixed
- Filter edge cases with null values
- Duration slider behavior with missing data
- Card height consistency in grid view
- Badge overflow on small screens
- Search state persistence

### 📚 Documentation
- Added installation instructions
- Created usage guides for TAs and students
- Documented all features with examples
- Added troubleshooting section
- Created customization guide with code examples
- Added deployment instructions

---

## [1.0.0] - Original Release

### ✨ Initial Features
- Course card display with gradient design
- Multi-select filtering system:
  - Competency Domain
  - Priority Skills
  - Level
  - Format
  - Student Journey Stage
  - Platform/Host
  - Duration slider
- Full-text search across titles and descriptions
- Stats dashboard with key metrics
- Course preview with expandable details
- Quick assign feature for TA recommendations
- Dark theme with Inter font
- Badge system for course attributes
- Duration parsing from various formats
- Hierarchical data handling (domain/focus areas)

### 🎨 Design
- Dark theme (#0f1117 background)
- Gradient cards with hover effects
- Color-coded badges for different attributes
- 3-column grid layout
- Responsive stat cards
- Custom CSS styling

### 🔧 Technical
- Streamlit framework
- Pandas for data manipulation
- CSV data source
- Caching for performance
- Forward-fill for hierarchical data
- Flexible duration parsing

---

## Version Comparison

| Feature | v1.0 | v2.0 |
|---------|------|------|
| View Options | Grid only | Grid + List |
| Sorting | None | 5 options |
| Export | None | CSV export |
| Insights | Basic | Enhanced |
| Documentation | None | Comprehensive |
| Configuration | Hardcoded | Config file |
| Animations | Basic | Enhanced |
| Mobile Support | Fair | Good |
| Customization | Hard | Easy |

---

## Upgrade Path

### From v1.0 to v2.0

1. **Backup current version**:
   ```bash
   cp app.py app.py.v1.backup
   ```

2. **Replace app.py** with new version

3. **Add new files**:
   - config.py
   - requirements.txt
   - README.md
   - QUICK_START.md
   - ENHANCEMENTS_GUIDE.md

4. **No data changes needed** - fully backward compatible

5. **Test**:
   ```bash
   streamlit run app.py
   ```

---

## Breaking Changes

### v2.0
- None! Fully backward compatible with v1.0

---

## Deprecations

### v2.0
- None

---

## Known Issues

### v2.0
- None reported

### v1.0
- No clear all filters option (fixed in v2.0)
- No export functionality (fixed in v2.0)
- Limited sorting options (fixed in v2.0)
- No view toggle (fixed in v2.0)

---

## Roadmap

### v2.1 (Planned)
- [ ] Pagination for large datasets
- [ ] Advanced search with operators
- [ ] Filter presets/saved searches
- [ ] Dark/light theme toggle

### v3.0 (Future)
- [ ] User authentication
- [ ] Course recommendations
- [ ] Rating and review system
- [ ] Progress tracking
- [ ] LMS integration

---

## Contributors

- Initial development: Course Explorer Team
- v2.0 enhancements: AI-assisted development

---

## License

Educational use - Carnegie Mellon University Student Success Support

---

## Support

For issues or questions:
1. Check QUICK_START.md for common issues
2. Review ENHANCEMENTS_GUIDE.md for customization
3. Contact Student Success team

---

**Last Updated**: 2024
**Current Version**: 2.0.0
**Status**: Stable
