"""
Theme styles for Course Explorer
Provides dark and light theme CSS
"""

def get_theme_css(theme='dark'):
    """Returns CSS based on selected theme"""
    
    if theme == 'light':
        return """
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── Global background ── */
.stApp { background: #f8fafc; color: #1e293b; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e2e8f0;
}
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p {
    color: #1e293b !important;
}
section[data-testid="stSidebar"] .block-container { 
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 0.5rem;
}
section[data-testid="stSidebar"] .stMultiSelect {
    margin-bottom: 0.75rem;
}
section[data-testid="stSidebar"] .stMultiSelect label {
    font-size: 0.85rem;
    margin-bottom: 0.25rem;
}
[data-baseweb="popover"] {
    max-height: 400px !important;
}
[data-baseweb="popover"] > div {
    max-height: 400px !important;
    overflow-y: auto !important;
}
section[data-testid="stSidebar"] > div:first-child {
    overflow-y: auto;
    max-height: 100vh;
}

/* ── Header ── */
.main-header {
    background: linear-gradient(135deg, #e0e7ff 0%, #dbeafe 100%);
    border: 1px solid #c7d2fe;
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
}
.main-header h1 {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #059669, #2563eb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.main-header .subtitle {
    color: #64748b;
    font-size: 0.9rem;
    margin-top: 0.5rem;
}

/* ── Stat cards row ── */
.stat-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.stat-card {
    flex: 1; min-width: 140px;
    background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    text-align: center;
    transition: transform .2s, box-shadow .2s;
}
.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,.1);
}
.stat-card .stat-value {
    font-size: 2rem; font-weight: 700;
    background: linear-gradient(90deg, #059669, #2563eb);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.stat-card .stat-label { font-size: 0.75rem; color: #64748b; margin-top: 2px; }

/* ── Course card ── */
.course-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1.25rem 1.4rem 1rem;
    height: 100%;
    transition: all .25s ease;
    position: relative;
    cursor: pointer;
}
.course-card:hover {
    border-color: #6366f1;
    box-shadow: 0 0 20px rgba(99,102,241,.15);
    transform: translateY(-4px);
}
.course-card .card-title {
    font-size: 1rem; font-weight: 600; color: #0f172a;
    margin-bottom: .5rem; line-height: 1.3;
}
.course-card .card-meta {
    font-size: 0.78rem; color: #64748b; margin-bottom: .6rem;
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
.badge-domain  { background:#dbeafe; color:#1e40af; }
.badge-level   { background:#d1fae5; color:#065f46; }
.badge-format  { background:#e9d5ff; color:#6b21a8; }
.badge-skill   { background:#fef3c7; color:#92400e; border:1px solid #fbbf24; }
.badge-journey { background:#fce7f3; color:#9f1239; }
.badge-platform { background:#cffafe; color:#0e7490; }

/* ── Description text ── */
.card-description {
    font-size: 0.82rem; color: #475569; line-height: 1.55;
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
    background: #f1f5f9;
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
    color: #1e40af;
    font-size: 0.85rem;
    margin: 1rem 0;
}

/* ── Theme Toggle Button ── */
.theme-toggle {
    position: fixed;
    top: 1rem;
    right: 1rem;
    z-index: 999;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 50%;
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(0,0,0,.1);
    transition: all .2s;
}
.theme-toggle:hover {
    transform: scale(1.1);
    box-shadow: 0 4px 12px rgba(0,0,0,.15);
}

/* ── Responsive adjustments ── */
@media (max-width: 768px) {
    .stat-card { min-width: 100%; }
    .main-header h1 { font-size: 1.5rem; }
}
</style>
"""
    else:  # dark theme
        return """
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── Global background ── */
.stApp { background: #0f1117; color: #e4e4e7; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #161b22;
    border-right: 1px solid #21262d;
}
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p {
    color: #e4e4e7 !important;
}
section[data-testid="stSidebar"] .block-container { 
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 0.5rem;
}
section[data-testid="stSidebar"] .stMultiSelect {
    margin-bottom: 0.75rem;
}
section[data-testid="stSidebar"] .stMultiSelect label {
    font-size: 0.85rem;
    margin-bottom: 0.25rem;
}
[data-baseweb="popover"] {
    max-height: 400px !important;
}
[data-baseweb="popover"] > div {
    max-height: 400px !important;
    overflow-y: auto !important;
}
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

/* ── Theme Toggle Button ── */
.theme-toggle {
    position: fixed;
    top: 1rem;
    right: 1rem;
    z-index: 999;
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 50%;
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(0,0,0,.3);
    transition: all .2s;
}
.theme-toggle:hover {
    transform: scale(1.1);
    box-shadow: 0 4px 12px rgba(0,0,0,.5);
}

/* ── Responsive adjustments ── */
@media (max-width: 768px) {
    .stat-card { min-width: 100%; }
    .main-header h1 { font-size: 1.5rem; }
}
</style>
"""
