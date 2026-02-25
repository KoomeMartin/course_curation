"""
Course Explorer — Student Success
Streamlit MVP for curated course discovery and TA assignment.
Run:  streamlit run app.py
"""

import re
import textwrap
import pandas as pd
import streamlit as st
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Course Explorer — Student Success",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS — premium card look, badges, responsive grid
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── Global background ── */
.stApp { background: #0f1117; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #161b22;
    border-right: 1px solid #21262d;
}
section[data-testid="stSidebar"] .block-container { 
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 0.5rem;
}
/* Compact multiselect styling */
section[data-testid="stSidebar"] .stMultiSelect {
    margin-bottom: 0.75rem;
}
section[data-testid="stSidebar"] .stMultiSelect label {
    font-size: 0.85rem;
    margin-bottom: 0.25rem;
}
/* Fix multiselect dropdown scrolling */
[data-baseweb="popover"] {
    max-height: 400px !important;
}
[data-baseweb="popover"] > div {
    max-height: 400px !important;
    overflow-y: auto !important;
}
/* Ensure sidebar itself is scrollable */
section[data-testid="stSidebar"] > div:first-child {
    overflow-y: auto;
    max-height: 100vh;
}

/* ── Header ── */
.main-header {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
}
.main-header h1 {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #6ee7b7, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.main-header .subtitle {
    color: #94a3b8;
    font-size: 0.9rem;
    margin-top: 0.5rem;
}

/* ── Stat cards row ── */
.stat-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.stat-card {
    flex: 1; min-width: 140px;
    background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
    border: 1px solid #374151;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    text-align: center;
    transition: transform .2s, box-shadow .2s;
}
.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,.3);
}
.stat-card .stat-value {
    font-size: 2rem; font-weight: 700;
    background: linear-gradient(90deg, #6ee7b7, #3b82f6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.stat-card .stat-label { font-size: 0.75rem; color: #9ca3af; margin-top: 2px; }

/* ── Course card ── */
.course-card {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 1.25rem 1.4rem 1rem;
    height: 100%;
    transition: all .25s ease;
    position: relative;
    cursor: pointer;
}
.course-card:hover {
    border-color: #6366f1;
    box-shadow: 0 0 20px rgba(99,102,241,.25);
    transform: translateY(-4px);
}
.course-card .card-title {
    font-size: 1rem; font-weight: 600; color: #f1f5f9;
    margin-bottom: .5rem; line-height: 1.3;
}
.course-card .card-meta {
    font-size: 0.78rem; color: #94a3b8; margin-bottom: .6rem;
}

/* ── Badges ── */
.badge {
    display: inline-block;
    padding: 3px 10px; border-radius: 999px;
    font-size: 0.7rem; font-weight: 600;
    margin: 2px 2px 4px 0;
    white-space: nowrap;
    letter-spacing: .4px;
    transition: transform .2s;
}
.badge:hover {
    transform: scale(1.05);
}
.badge-domain  { background:#1d4ed8; color:#bfdbfe; }
.badge-level   { background:#065f46; color:#a7f3d0; }
.badge-format  { background:#6d28d9; color:#ddd6fe; }
.badge-skill   { background:#92400e; color:#fde68a; border:1px solid #78350f; }
.badge-journey { background:#be185d; color:#fce7f3; }
.badge-platform { background:#0e7490; color:#a5f3fc; }

/* ── Description text ── */
.card-description {
    font-size: 0.82rem; color: #cbd5e1; line-height: 1.55;
    margin: .5rem 0 .9rem;
    display: -webkit-box; -webkit-line-clamp: 3;
    -webkit-box-orient: vertical; overflow: hidden;
}

/* ── Duration / format line ── */
.card-sub { font-size: 0.75rem; color: #64748b; margin-bottom: .75rem; }

/* ── Expander tweak ── */
details summary { font-size: .85rem !important; }

/* ── Filter section ── */
.filter-section {
    background: #1a1f2e;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1rem;
}

/* ── Alert boxes ── */
.info-box {
    background: rgba(59, 130, 246, 0.1);
    border-left: 3px solid #3b82f6;
    padding: 0.75rem 1rem;
    border-radius: 4px;
    color: #93c5fd;
    font-size: 0.85rem;
    margin: 1rem 0;
}

/* ── Responsive adjustments ── */
@media (max-width: 768px) {
    .stat-card { min-width: 100%; }
    .main-header h1 { font-size: 1.5rem; }
}
</style>
""",
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING & NORMALIZATION
# ─────────────────────────────────────────────────────────────────────────────

RAW_COLS = {
    "Competency domain":         "domain",
    "Focus Areas":               "focus_area",
    "Resource title":            "title",
    "URL":                       "lms_link",
    "Platform / host":           "platform",
    "Resource type":             "resource_type",
    "Stated learning outcomes":  "full_description",
    "Stated prerequisites":      "prerequisites",
    "Length (mins)":             "length_raw",
    "Indicated level":           "level",
    "Intended audience":         "audience",
    "Format type (passive / interactive)": "format",
    "Publication date":          "publication_date",
    "Last updated":              "last_updated",
    "Captions / transcripts":    "captions",
    "Mobile accessible":         "mobile_accessible",
    "Skill area":                "priority_skills",
    "Student journey stage":     "journey_stage",
    "Comments":                  "comments",
}


def _parse_duration_hours(raw: str) -> float | None:
    """Convert heterogeneous duration strings → approximate hours (float)."""
    if not isinstance(raw, str) or not raw.strip():
        return None
    s = raw.lower().strip()

    # patterns: "16 hours", "5 hours a day for 3 days", "12 weeks", "1 year",
    #           "one semester", "35 videos roughly 50 mins each",
    #           "16 videos roughly 4–17 min each", "5hrs", "5hours", "4 hrs"
    patterns = [
        (r"(\d+(?:\.\d+)?)\s*hours?\s*a\s*day\s*for\s*(\d+)\s*days?", lambda m: float(m.group(1)) * int(m.group(2))),
        (r"(\d+(?:\.\d+)?)\s*hrs?\b", lambda m: float(m.group(1))),
        (r"(\d+(?:\.\d+)?)\s*hours?\b", lambda m: float(m.group(1))),
        (r"(\d+)\s*videos?\s*roughly\s*([\d.]+)\s*[-–]\s*([\d.]+)\s*min",
         lambda m: int(m.group(1)) * (float(m.group(2)) + float(m.group(3))) / 2 / 60),
        (r"(\d+)\s*videos?\s*roughly\s*([\d.]+)\s*min", lambda m: int(m.group(1)) * float(m.group(2)) / 60),
        (r"(\d+(?:\.\d+)?)\s*min(?:utes?)?\b", lambda m: float(m.group(1)) / 60),
        (r"(\d+)\s*weeks?\b", lambda m: float(m.group(1)) * 5),     # ~5 hrs/week light estimate
        (r"one\s+semester|a\s+semester", lambda m: 45.0),
        (r"half\s+a\s+semester", lambda m: 22.5),
        (r"(\d+)\s*months?\b", lambda m: float(m.group(1)) * 10),
        (r"(\d+)\s*years?\b", lambda m: float(m.group(1)) * 120),
    ]
    for pattern, fn in patterns:
        m = re.search(pattern, s)
        if m:
            try:
                return round(fn(m), 1)
            except Exception:
                continue
    return None


@st.cache_data(show_spinner="Loading course catalogue…")
def load_data(path: str = "Online_curation.csv") -> pd.DataFrame:
    raw = pd.read_csv(path, dtype=str)

    # Forward-fill the hierarchical domain & focus area columns
    raw["Competency domain"] = raw["Competency domain"].replace("", pd.NA).ffill()
    raw["Focus Areas"] = raw["Focus Areas"].replace("", pd.NA).ffill()

    # Rename
    raw = raw.rename(columns=RAW_COLS)

    # Drop rows with no title
    df = raw.dropna(subset=["title"]).copy()
    df = df[df["title"].str.strip() != ""].copy()
    df = df.reset_index(drop=True)
    df["id"] = df.index

    # Clean text columns
    for col in ["domain", "focus_area", "level", "format", "journey_stage",
                 "priority_skills", "platform", "resource_type"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().replace({"nan": "", "N/A": "", "Not Stated": ""})

    # Short description: first 250 chars of learning outcomes
    df["short_description"] = df["full_description"].fillna("").apply(
        lambda s: textwrap.shorten(s.replace("\n", " ").strip(), width=250, placeholder="…")
    )

    # Parse duration
    df["duration_hours"] = df["length_raw"].apply(_parse_duration_hours)

    # Normalize skill tags (may be long sentences — truncate for tags)
    def _skill_tags(s) -> list[str]:
        # Handle non-string types
        if pd.isna(s) or not s:
            return []
        s = str(s)
        if s.strip() in ("", "nan", "None"):
            return []
        # If it looks like a sentence (contains comma-separated brief things), split on comma
        parts = [p.strip() for p in s.split(",") if p.strip()]
        # Truncate very long parts to ~50 chars for display
        return [str(p)[:60] + ("…" if len(str(p)) > 60 else "") for p in parts]

    df["skill_tags"] = df["priority_skills"].fillna("").apply(_skill_tags)

    return df


df = load_data()

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Filters")
    st.caption("Narrow the course catalogue")

    # Search with clear button
    col1, col2 = st.columns([4, 1])
    with col1:
        search_q = st.text_input("Search title / description", placeholder="e.g. Python, statistics…", label_visibility="visible")
    with col2:
        st.markdown("<div style='margin-top: 1.8rem;'></div>", unsafe_allow_html=True)
        if st.button("🗑️", help="Clear search"):
            search_q = ""

    st.markdown("---")
    st.markdown("### 📚 Course Attributes")

    domains = sorted({d for d in df["domain"].unique() if d})
    sel_domains = st.multiselect("Competency Domain", domains, help="Filter by subject area")

    all_skills: list[str] = sorted(
        {tag for tags in df["skill_tags"] for tag in tags}
    )
    sel_skills = st.multiselect("Priority Skills", all_skills, help="Filter by specific skills")

    levels = sorted({l for l in df["level"].unique() if l})
    sel_levels = st.multiselect("Level", levels, help="Beginner, Intermediate, Advanced")

    formats = sorted({f for f in df["format"].unique() if f})
    sel_formats = st.multiselect("Format", formats, help="Interactive or Passive")

    journey_opts = sorted({j for j in df["journey_stage"].unique() if j})
    sel_journey = st.multiselect("Student Journey Stage", journey_opts, help="Pre-arrival, Ongoing study, etc.")

    platforms = sorted({p for p in df["platform"].unique() if p})
    sel_platforms = st.multiselect("Platform / Host", platforms, help="OLI, DataQuest, etc.")

    # Duration slider — only if we have parsed values
    dur_df = df["duration_hours"].dropna()
    if not dur_df.empty:
        dur_min_v = float(dur_df.min())
        dur_max_v = float(dur_df.max())
        if dur_min_v < dur_max_v:
            sel_dur = st.slider(
                "Duration (hours)",
                min_value=dur_min_v,
                max_value=dur_max_v,
                value=(dur_min_v, dur_max_v),
                step=0.5,
                help="Filter by course duration"
            )
        else:
            sel_dur = None
    else:
        sel_dur = None

    st.markdown("---")
    show_no_link = st.checkbox("Show courses without links", value=True)
    
    # Clear all filters button
    st.markdown("---")
    if st.button("🔄 Clear All Filters", use_container_width=True):
        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# FILTERING LOGIC
# ─────────────────────────────────────────────────────────────────────────────
mask = pd.Series(True, index=df.index)

if search_q:
    q_low = search_q.lower()
    mask &= (
        df["title"].str.lower().str.contains(q_low, na=False)
        | df["short_description"].str.lower().str.contains(q_low, na=False)
        | df["full_description"].fillna("").str.lower().str.contains(q_low, na=False)
    )

if sel_domains:
    mask &= df["domain"].isin(sel_domains)

if sel_skills:
    mask &= df["skill_tags"].apply(
        lambda tags: any(
            any(sel.lower() in tag.lower() for tag in tags) for sel in sel_skills
        )
    )

if sel_levels:
    mask &= df["level"].isin(sel_levels)

if sel_formats:
    mask &= df["format"].str.lower().isin([f.lower() for f in sel_formats])

if sel_journey:
    mask &= df["journey_stage"].isin(sel_journey)

if sel_platforms:
    mask &= df["platform"].isin(sel_platforms)

if sel_dur is not None:
    lo, hi = sel_dur
    # Include rows without parsed duration unless explicitly filtered
    dur_mask = df["duration_hours"].isna() | df["duration_hours"].between(lo, hi)
    mask &= dur_mask

if not show_no_link:
    mask &= df["lms_link"].notna() & (df["lms_link"].str.strip() != "")

filtered = df[mask].copy()

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🎓 Course Explorer — Student Success</h1>
    <div class="subtitle">Curated resources aligned to program competencies · For TA-assisted advising</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# QUICK STATS
# ─────────────────────────────────────────────────────────────────────────────
all_tags_flat = [tag for tags in df["skill_tags"] for tag in tags]
from collections import Counter
top_skills = [s for s, _ in Counter(all_tags_flat).most_common(5)]

# Duration coverage
dur_count = int(df["duration_hours"].notna().sum())

stats_html = f"""
<div class="stat-row">
  <div class="stat-card">
    <div class="stat-value">{len(df)}</div>
    <div class="stat-label">Total Courses</div>
  </div>
  <div class="stat-card">
    <div class="stat-value">{df['domain'].nunique()}</div>
    <div class="stat-label">Domains</div>
  </div>
  <div class="stat-card">
    <div class="stat-value">{df['platform'].nunique()}</div>
    <div class="stat-label">Platforms</div>
  </div>
  <div class="stat-card">
    <div class="stat-value">{len(filtered)}</div>
    <div class="stat-label">Showing Now</div>
  </div>
  <div class="stat-card" style="min-width:260px; text-align:left;">
    <div class="stat-label" style="margin-bottom:4px;">Top Skill Areas</div>
    <div style="display: flex; flex-wrap: wrap; gap: 4px; margin-top: 8px;">
      {"".join(f'<span class="badge badge-skill" style="font-size:.65rem;">{str(s)[:35]}</span>' for s in top_skills if s)}
    </div>
  </div>
</div>
"""
st.markdown(stats_html, unsafe_allow_html=True)
st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# RESULT COUNT & SORTING
# ─────────────────────────────────────────────────────────────────────────────
if filtered.empty:
    st.warning("No courses match your filters. Try widening your search.")
    st.stop()

# Sorting and view options
col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
with col1:
    st.markdown(
        f"<p style='color:#94a3b8; font-size:.85rem; margin-top: 0.5rem;'>Showing <b style='color:#f1f5f9'>{len(filtered)}</b> of {len(df)} courses</p>",
        unsafe_allow_html=True,
    )
with col2:
    sort_by = st.selectbox(
        "Sort by",
        ["Relevance", "Duration (Low to High)", "Duration (High to Low)", "Title (A-Z)", "Title (Z-A)"],
        label_visibility="collapsed"
    )
with col3:
    view_mode = st.selectbox("View", ["Grid", "List"], label_visibility="collapsed")
with col4:
    # Export to CSV
    csv_data = filtered[["title", "domain", "platform", "level", "format", "duration_hours", "lms_link", "short_description"]].to_csv(index=False)
    st.download_button(
        label="📥 Export",
        data=csv_data,
        file_name=f"courses_export_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# Apply sorting
if sort_by == "Duration (Low to High)":
    filtered = filtered.sort_values("duration_hours", na_position='last')
elif sort_by == "Duration (High to Low)":
    filtered = filtered.sort_values("duration_hours", ascending=False, na_position='last')
elif sort_by == "Title (A-Z)":
    filtered = filtered.sort_values("title")
elif sort_by == "Title (Z-A)":
    filtered = filtered.sort_values("title", ascending=False)

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# CARD GRID — 3 columns or list view
# ─────────────────────────────────────────────────────────────────────────────
DOMAIN_COLORS = [
    "#1d4ed8", "#6d28d9", "#0e7490", "#065f46", "#92400e",
    "#be185d", "#b45309", "#1e3a5f", "#4a044e", "#134e4a",
]
domain_list = sorted({d for d in df["domain"].unique() if d})
domain_color_map = {d: DOMAIN_COLORS[i % len(DOMAIN_COLORS)] for i, d in enumerate(domain_list)}

if view_mode == "Grid":
    COLS = 3
    rows = [filtered.iloc[i: i + COLS] for i in range(0, len(filtered), COLS)]
else:
    COLS = 1
    rows = [filtered.iloc[i: i + COLS] for i in range(0, len(filtered), COLS)]

for row_batch in rows:
    cols = st.columns(COLS)
    for col, (_, row) in zip(cols, row_batch.iterrows()):
        with col:
            domain_val = row.get("domain", "") or ""
            level_val  = row.get("level", "")  or ""
            fmt_val    = row.get("format", "")  or ""
            journey    = row.get("journey_stage", "") or ""
            platform   = row.get("platform", "") or ""
            link       = row.get("lms_link", "")  or ""
            dur_h      = row.get("duration_hours")
            res_type   = row.get("resource_type", "") or ""
            desc       = row.get("short_description", "") or ""
            full_desc  = row.get("full_description", "") or ""
            prereqs    = row.get("prerequisites", "") or ""
            skills     = row.get("skill_tags", []) or []
            title      = row.get("title", "(Untitled)")
            
            # Ensure all string fields are actually strings
            domain_val = str(domain_val) if pd.notna(domain_val) else ""
            level_val = str(level_val) if pd.notna(level_val) else ""
            fmt_val = str(fmt_val) if pd.notna(fmt_val) else ""
            journey = str(journey) if pd.notna(journey) else ""
            platform = str(platform) if pd.notna(platform) else ""
            link = str(link) if pd.notna(link) else ""
            res_type = str(res_type) if pd.notna(res_type) else ""
            desc = str(desc) if pd.notna(desc) else ""
            full_desc = str(full_desc) if pd.notna(full_desc) else ""
            prereqs = str(prereqs) if pd.notna(prereqs) else ""
            title = str(title) if pd.notna(title) else "(Untitled)"

            # Domain color
            d_color = domain_color_map.get(domain_val, "#374151")
            d_fg = "#bfdbfe"

            # Duration display
            if dur_h is not None:
                if dur_h >= 100:
                    dur_display = f"~{int(dur_h/10)*10}h est."
                else:
                    dur_display = f"{dur_h}h"
            else:
                dur_display = row.get("length_raw", "") or "Duration TBD"

            # Build badge HTML
            badges = ""
            if domain_val and domain_val.strip():
                badges += f'<span class="badge badge-domain">{str(domain_val)[:30]}</span>'
            if level_val and level_val.strip():
                badges += f'<span class="badge badge-level">{str(level_val)}</span>'
            if fmt_val and fmt_val.strip():
                badges += f'<span class="badge badge-format">{str(fmt_val)}</span>'
            if journey and journey.strip():
                badges += f'<span class="badge badge-journey">{str(journey)}</span>'
            if platform and platform.strip():
                badges += f'<span class="badge badge-platform">{str(platform)[:20]}</span>'

            card_html = f"""
<div class="course-card">
  <div class="card-title">{title}</div>
  <div>{badges}</div>
  <div class="card-sub">📦 {platform or res_type or '—'} · ⏱ {dur_display}</div>
  <div class="card-description">{desc or '<em style="color:#64748b">No description available.</em>'}</div>
</div>
"""
            st.markdown(card_html, unsafe_allow_html=True)

            # ── Clickable card with dialog ────────────────────────────────
            if st.button("View Details", key=f"view_{row['id']}", use_container_width=True, type="primary"):
                with st.expander("📖 Course Details", expanded=True):
                    st.markdown(f"### {title}")
                    
                    # Course metadata in columns
                    meta_col1, meta_col2 = st.columns(2)
                    with meta_col1:
                        if domain_val and domain_val.strip():
                            st.markdown(f"**Domain:** {domain_val}")
                        if platform and platform.strip():
                            st.markdown(f"**Platform:** {platform}")
                        if level_val and level_val.strip():
                            st.markdown(f"**Level:** {level_val}")
                    with meta_col2:
                        if fmt_val and fmt_val.strip():
                            st.markdown(f"**Format:** {fmt_val}")
                        if dur_display:
                            st.markdown(f"**Duration:** {dur_display}")
                        if journey and journey.strip():
                            st.markdown(f"**Journey Stage:** {journey}")
                    
                    st.markdown("---")
                    
                    # Learning outcomes
                    if full_desc and isinstance(full_desc, str) and full_desc.strip() and full_desc not in ("nan", "None"):
                        st.markdown("**Learning Outcomes:**")
                        st.markdown(full_desc[:800] + ("…" if len(full_desc) > 800 else ""))
                    
                    # Prerequisites
                    if prereqs and isinstance(prereqs, str) and prereqs.strip() and prereqs not in ("nan", "N/A", "None", ""):
                        st.markdown("**Prerequisites:**")
                        st.markdown(prereqs[:300])
                    
                    # Skills - only show if they're actual skills, not long descriptions
                    if skills and len(skills) > 0:
                        # Filter out very long skill descriptions (likely the competency text)
                        clean_skills = [s for s in skills if len(s) < 100]
                        if clean_skills:
                            st.markdown("**Skills Covered:**")
                            st.markdown(", ".join(clean_skills[:10]))  # Limit to 10 skills
                    
                    st.markdown("---")
                    
                    # Course link
                    if link and link.strip() and link not in ("nan", "None", ""):
                        st.link_button("🔗 Open Course", link, use_container_width=True)
                    else:
                        st.info("No course link available.")

            st.markdown("<div style='margin-bottom:1.2rem;'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")

# Quick insights about filtered data
if len(filtered) > 0:
    avg_duration = filtered["duration_hours"].mean()
    most_common_platform = filtered["platform"].mode()[0] if not filtered["platform"].mode().empty else "N/A"
    most_common_level = filtered["level"].mode()[0] if not filtered["level"].mode().empty else "N/A"
    
    insight_col1, insight_col2, insight_col3 = st.columns(3)
    with insight_col1:
        st.markdown(f"""
        <div class="info-box">
            <strong>📊 Average Duration</strong><br>
            {f'{avg_duration:.1f} hours' if pd.notna(avg_duration) else 'N/A'}
        </div>
        """, unsafe_allow_html=True)
    with insight_col2:
        st.markdown(f"""
        <div class="info-box">
            <strong>🏆 Most Common Platform</strong><br>
            {most_common_platform}
        </div>
        """, unsafe_allow_html=True)
    with insight_col3:
        st.markdown(f"""
        <div class="info-box">
            <strong>📈 Most Common Level</strong><br>
            {most_common_level}
        </div>
        """, unsafe_allow_html=True)

st.markdown(
    "<p style='text-align:center; color:#475569; font-size:.8rem; margin-top: 2rem;'>"
    "Course Explorer MVP · Student Success Support · CMU · "
    f"Catalogue: {len(df)} resources across {df['domain'].nunique()} domains"
    "</p>",
    unsafe_allow_html=True,
)
