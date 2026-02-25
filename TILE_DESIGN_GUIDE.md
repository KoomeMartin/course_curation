# 📐 Tile Design Guide

Visual guide for the Course Explorer tile design philosophy and implementation.

---

## Design Philosophy

### Core Principle: "Brief but Informative"

Each tile should answer these questions at a glance:
1. **What is it?** → Title
2. **What type?** → Domain, Level, Format badges
3. **Where?** → Platform
4. **How long?** → Duration
5. **What's it about?** → Brief description

Everything else → Details view (on click)

---

## Tile Anatomy

```
┌─────────────────────────────────────────────┐
│ 1. TITLE                                    │ ← Course name
│ ─────────────────────────────────────────── │
│ 2. BADGES                                   │ ← Quick categorization
│    [Domain] [Level] [Format] [Journey]     │
│ ─────────────────────────────────────────── │
│ 3. METADATA                                 │ ← Platform & time
│    📦 Platform · ⏱ Duration                 │
│ ─────────────────────────────────────────── │
│ 4. DESCRIPTION                              │ ← Brief overview
│    Short preview of what the course         │
│    covers in 2-3 lines...                   │
│ ─────────────────────────────────────────── │
│                                             │
│ 5. ACTION                                   │ ← Single clear action
│    [        View Details        ]           │
│                                             │
└─────────────────────────────────────────────┘
```

---

## Information Hierarchy

### Level 1: Immediate (Tile)
**Purpose**: Quick scanning and filtering
**Content**:
- Course title (1 line, truncated if needed)
- Category badges (4-5 max)
- Platform & duration (1 line)
- Description (2-3 lines, ~250 chars)

**NOT Included**:
- ❌ Long skill descriptions
- ❌ Learning outcomes
- ❌ Prerequisites
- ❌ Full course details

---

### Level 2: On Demand (Details View)
**Purpose**: Comprehensive information before enrollment
**Content**:
- Full course title
- All metadata (organized in columns)
- Learning outcomes (800 chars)
- Prerequisites (300 chars)
- Clean skills list (10 max)
- Direct course link

---

## Badge System

### Badge Types & Colors

1. **Domain Badge** (Blue)
   - Purpose: Subject area
   - Example: "Data Science", "Programming"
   - Color: `#1d4ed8`

2. **Level Badge** (Green)
   - Purpose: Difficulty
   - Example: "Beginner", "Advanced"
   - Color: `#065f46`

3. **Format Badge** (Purple)
   - Purpose: Learning style
   - Example: "Interactive", "Passive"
   - Color: `#6d28d9`

4. **Journey Badge** (Pink)
   - Purpose: When to take
   - Example: "Pre-arrival", "Ongoing study"
   - Color: `#be185d`

5. **Platform Badge** (Cyan)
   - Purpose: Course provider
   - Example: "OLI", "DataQuest"
   - Color: `#0e7490`

### Badge Rules
- Maximum 5 badges per tile
- Truncate long text (20-30 chars)
- Consistent order: Domain → Level → Format → Journey → Platform
- Hover effect for interactivity

---

## Content Guidelines

### Title
- **Length**: 1-2 lines maximum
- **Style**: Bold, prominent
- **Truncation**: Use ellipsis if too long
- **Example**: "Introduction to Python Programming"

### Description
- **Length**: 2-3 lines (~250 characters)
- **Content**: Brief overview, not full outcomes
- **Style**: Regular text, readable
- **Truncation**: "…" at end if longer
- **Example**: "Learn Python basics including variables, loops, and functions. Build practical projects to apply your knowledge."

### Platform & Duration
- **Format**: `📦 Platform · ⏱ Duration`
- **Platform**: Name or resource type
- **Duration**: Parsed hours or original text
- **Example**: `📦 OLI · ⏱ 5h`

---

## What NOT to Show on Tiles

### ❌ Long Skill Descriptions
**Bad**:
```
Skills: Demonstrate the ability to apply programming 
skills and software engineering knowledge, including 
data structures and algorithms, to practical problems.
```

**Why**: Too verbose, clutters tile, hard to scan

**Solution**: Show in details view, filtered to < 100 chars

---

### ❌ Full Learning Outcomes
**Bad**:
```
By the end of this course, students will be able to:
1. Understand fundamental concepts...
2. Apply techniques to real-world...
3. Analyze and evaluate...
[continues for 500+ words]
```

**Why**: Too long for quick browsing

**Solution**: Show brief description on tile, full outcomes in details

---

### ❌ Multiple Action Buttons
**Bad**:
```
[Preview] [Quick Assign] [Bookmark] [Share]
```

**Why**: Cluttered, confusing, competing actions

**Solution**: Single "View Details" button

---

## Spacing & Layout

### Vertical Spacing
```
Title
↓ 0.5rem
Badges
↓ 0.75rem
Platform/Duration
↓ 0.75rem
Description
↓ 0.9rem
Button
↓ 1.2rem (between cards)
```

### Padding
- Card: `1.25rem 1.4rem 1rem`
- Consistent internal spacing
- Breathing room around content

### Hover Effect
- Border color: `#6366f1` (purple)
- Shadow: `0 0 20px rgba(99,102,241,.25)`
- Transform: `translateY(-4px)` (lift effect)
- Cursor: `pointer`

---

## Responsive Behavior

### Desktop (> 1024px)
- 3 columns
- Full card width
- All content visible

### Tablet (768px - 1024px)
- 2 columns
- Adjusted card width
- Same content

### Mobile (< 768px)
- 1 column
- Full width cards
- Same content, stacked

---

## Accessibility

### Color Contrast
- Text on dark background: `#f1f5f9`
- Secondary text: `#94a3b8`
- Meets WCAG AA standards

### Interactive Elements
- Clear focus states
- Keyboard navigable
- Screen reader friendly labels
- Touch targets > 44px

### Semantic HTML
- Proper heading hierarchy
- Descriptive button labels
- Alt text where needed

---

## Performance Considerations

### Optimization
- Minimal HTML per card
- CSS-based styling (no images)
- Efficient rendering
- Lazy loading for large lists

### Metrics
- ~15 DOM elements per card
- < 2KB HTML per card
- Fast hover interactions
- Smooth scrolling

---

## Common Mistakes to Avoid

### ❌ Too Much Information
**Problem**: Trying to show everything on the tile
**Solution**: Keep it brief, details on demand

### ❌ Inconsistent Layout
**Problem**: Different cards have different structures
**Solution**: Strict template for all cards

### ❌ Poor Hierarchy
**Problem**: All text looks the same
**Solution**: Clear visual hierarchy with size/weight

### ❌ Cluttered Badges
**Problem**: Too many badges, long text
**Solution**: Max 5 badges, truncate long text

### ❌ Weak Call-to-Action
**Problem**: Unclear what to do next
**Solution**: Single, prominent "View Details" button

---

## Design Checklist

Before adding any element to a tile, ask:

- [ ] Is this essential for quick scanning?
- [ ] Can this wait for the details view?
- [ ] Does this help users make decisions?
- [ ] Is this brief enough (< 3 lines)?
- [ ] Does this maintain visual balance?
- [ ] Is this consistent with other tiles?

If any answer is "No", move it to details view.

---

## Future Considerations

### Potential Additions (if needed)
- ⭐ Favorite/bookmark icon (top-right corner)
- 👥 Enrollment count (if available)
- ⏰ Last updated date (subtle, bottom)
- 🎯 Difficulty indicator (visual)

### NOT Recommended
- ❌ Multiple buttons
- ❌ Long text blocks
- ❌ Complex interactions
- ❌ Auto-expanding content
- ❌ Embedded videos/images

---

## Summary

**Perfect Tile Formula**:
```
Title (1-2 lines)
+ Badges (4-5 max)
+ Platform & Duration (1 line)
+ Description (2-3 lines)
+ Single Action Button
= Clean, Scannable, Professional
```

**Key Principle**: If it's not essential for quick decision-making, it belongs in the details view.

---

**Version**: 2.1.1
**Last Updated**: 2024
**Status**: ✅ Finalized
