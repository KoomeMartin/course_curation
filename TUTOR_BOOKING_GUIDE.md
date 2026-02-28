# 👥 Peer Tutor Booking Feature

## Overview
A lightweight peer tutor booking system integrated into the Course Explorer app. Students can find tutors based on Focus Areas and book sessions directly through Google Calendar.

## How It Works

### User Flow
1. **Click "Get Peer Tutor Support"** button in the main interface
2. **Select Focus Area** from dropdown (populated from course Focus Areas column)
3. **View Matching Tutors** displayed as cards with:
   - Tutor name
   - Expertise tags (matching Focus Areas)
   - Availability summary
   - Booking button
4. **Click "Book Session"** to open tutor's Google Calendar appointment page
5. **Google Calendar handles** the actual booking, notifications, and scheduling

### Key Features
- ✅ Simple, lightweight implementation
- ✅ No backend scheduling logic
- ✅ No database required
- ✅ Real-time booking through Google Calendar
- ✅ Automatic email notifications (via Google Calendar)
- ✅ Responsive tutor cards with enhanced styling
- ✅ Focus Area-based filtering (aligned with course data)
- ✅ Theme-aware design (dark/light mode)
- ✅ Animated buttons with gradient styling

## Data Structure

### Tutors CSV (`tutors.csv`)
Required columns:
- `tutor_id`: Unique identifier
- `tutor_name`: Full name of tutor
- `expertise_tags`: Comma-separated list of Focus Areas (e.g., "Programming Fundamentals, Software Development, Data Science")
- `availability_summary`: Human-readable availability (e.g., "Mon-Fri 2-6pm EST")
- `booking_link`: Google Calendar Appointment Scheduling URL

### Example Row
```csv
1,Martin Koome,"Programming Fundamentals, Software Development, Data Science",Available Mon-Fri 2-6pm EST,https://calendar.app.google/41nyw2ymf4xHGicf7
```

### Current Tutors
- **Martin Koome**: Programming Fundamentals, Software Development, Data Science
- **Paul**: AI & ML, Math Foundations, Data Science
- **Berket**: Cybersecurity, Networking, Software Development

## Setup Instructions

### 1. Create Google Calendar Appointment Schedules

For each tutor:

1. Go to [Google Calendar](https://calendar.google.com)
2. Click the **+** button → **Appointment schedule**
3. Configure:
   - **Title**: "Peer Tutoring Session with [Tutor Name]"
   - **Duration**: 30 min, 60 min, etc.
   - **Availability**: Set available time slots
   - **Booking window**: How far in advance students can book
   - **Buffer time**: Time between sessions
4. Click **Next** → **Save**
5. Copy the **booking page URL**
6. Add URL to `tutors.csv` for that tutor

### 2. Update Tutors Data

Edit `tutors.csv` with your actual tutors:

```csv
tutor_id,tutor_name,expertise_tags,availability_summary,booking_link
1,John Doe,"Python, Machine Learning, Data Science",Mon/Wed/Fri 3-6pm,https://calendar.google.com/calendar/appointments/schedules/YOUR_ACTUAL_LINK
2,Jane Smith,"Web Development, JavaScript, React",Tue/Thu 2-5pm,https://calendar.google.com/calendar/appointments/schedules/YOUR_ACTUAL_LINK
```

### 3. Run the App

```bash
streamlit run app.py
```

## Customization

### Adding More Focus Areas
Focus Areas are automatically pulled from the course data (`Focus Areas` column). The available options are:
- AI & ML
- Cybersecurity
- Data Science
- Electronics and Energy Fundamentals
- Hardware
- Math Foundations
- Networking
- Programming Fundamentals
- Simulation and Modelling
- Software
- Software Development

To add tutors for new focus areas, simply add them to the course data or update tutor expertise tags to match existing focus areas.

### Changing Card Layout
Modify `cols_per_row` variable in the tutor display section:
```python
cols_per_row = 3  # Change to 2 or 4 for different layouts
```

### Styling Tutor Cards
Tutor cards use the same CSS classes as course cards:
- `.course-card` - Main card styling
- `.card-title` - Tutor name
- `.badge-skill` - Expertise tags
- `.card-sub` - Availability text

## Constraints & Limitations

### What This Does NOT Do
- ❌ No ticketing system
- ❌ No booking database
- ❌ No calendar sync logic
- ❌ No status tracking
- ❌ No admin dashboard
- ❌ No Gmail API integration
- ❌ No payment processing

### What Google Calendar Handles
- ✅ Scheduling
- ✅ Email notifications
- ✅ Calendar invites
- ✅ Reminders
- ✅ Rescheduling
- ✅ Cancellations
- ✅ Time zone handling

### Troubleshooting

### No Tutors Found
**Issue**: "No tutors found with expertise in [Focus Area]"

**Solutions**:
1. Check that tutor expertise tags match course Focus Areas exactly
2. Ensure expertise tags are comma-separated
3. Verify `tutors.csv` is in the same directory as `app.py`
4. Focus Areas are case-sensitive - ensure they match the course data

### Booking Link Not Working
**Issue**: Clicking "Book Session" doesn't open calendar

**Solutions**:
1. Verify Google Calendar appointment schedule is published
2. Check that booking link is correct in `tutors.csv`
3. Ensure link starts with `https://calendar.google.com/`

### Tutors CSV Not Loading
**Issue**: App shows no tutors or errors

**Solutions**:
1. Verify `tutors.csv` exists in project root
2. Check CSV format matches required columns
3. Ensure no special characters in CSV data
4. Check file encoding is UTF-8

## Scaling Considerations

### For Small Teams (1-20 tutors)
- ✅ Current CSV approach works well
- ✅ Easy to maintain manually
- ✅ No infrastructure needed

### For Medium Teams (20-100 tutors)
- Consider Google Sheets integration
- Use `st.connection` to read from Google Sheets
- Tutors can update their own availability

### For Large Teams (100+ tutors)
- Consider a lightweight database (Airtable, Supabase)
- Add tutor profiles with photos
- Implement rating/review system
- Add search and advanced filtering

## Future Enhancements (Optional)

### Easy Additions
- [ ] Tutor profile photos
- [ ] Student ratings/reviews
- [ ] Favorite tutors
- [ ] Session history (via Google Calendar API)
- [ ] Email reminders (via Google Calendar)

### Advanced Features
- [ ] Real-time availability checking
- [ ] Group tutoring sessions
- [ ] Video call integration (Zoom/Meet links)
- [ ] Tutor analytics dashboard
- [ ] Automated matching algorithm

## Support

For issues or questions:
1. Check this guide first
2. Review `tutors.csv` format
3. Verify Google Calendar setup
4. Test with sample data provided

## Sample Data

The app includes 3 peer tutors:
- **Martin Koome** - Real booking link configured
- **Paul** - Placeholder booking link (needs to be updated)
- **Berket** - Placeholder booking link (needs to be updated)

Replace placeholder booking links with actual Google Calendar appointment schedule URLs.

---

**Built with**: Streamlit + Google Calendar  
**Complexity**: Minimal (MVP-level)  
**Maintenance**: Low (CSV-based)  
**Focus Areas**: Aligned with course Focus Areas column
