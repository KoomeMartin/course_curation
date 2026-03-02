"""
chatbot_1.py — Course Discovery Chatbot (Native Streamlit UI)
Full-page chatbot that renders in the main body area.
Backend uses Groq (llama-3.3-70b-versatile).

Usage in app_1.py:
    from chatbot_1 import render_chatbot
    render_chatbot(df, theme=st.session_state.theme)
"""

import json
import os
import re
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
from groq import Groq

load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# GROQ CLIENT
# ─────────────────────────────────────────────────────────────────────────────
client = Groq()
MODEL  = "llama-3.3-70b-versatile"

# ─────────────────────────────────────────────────────────────────────────────
# COLUMN MAP
# ─────────────────────────────────────────────────────────────────────────────
COL = {
    "domain":            "Competency domain",
    "focus_area":        "Focus Areas",
    "title":             "Resource title",
    "lms_link":          "URL",
    "platform":          "Platform / host",
    "resource_type":     "Resource type",
    "full_description":  "Stated learning outcomes",
    "prerequisites":     "Stated prerequisites",
    "length_raw":        "Length (mins)",
    "level":             "Indicated level",
    "audience":          "Intended audience",
    "format":            "Format type (passive / interactive)",
    "publication_date":  "Publication date",
    "last_updated":      "Last updated",
    "captions":          "Captions / transcripts",
    "mobile_accessible": "Mobile accessible",
    "priority_skills":   "Skill area",
    "journey_stage":     "Student journey stage",
    "comments":          "Comments",
}


def _col(df: pd.DataFrame, key: str) -> str:
    return COL[key] if COL[key] in df.columns else ""


# ─────────────────────────────────────────────────────────────────────────────
# SMART PRE-FILTER
# ─────────────────────────────────────────────────────────────────────────────
DURATION_KEYWORDS = {
    "long":          ("gte", 120),
    "lengthy":       ("gte", 120),
    "comprehensive": ("gte", 120),
    "in-depth":      ("gte", 120),
    "in depth":      ("gte", 120),
    "detailed":      ("gte", 90),
    "extensive":     ("gte", 180),
    "full":          ("gte", 120),
    "complete":      ("gte", 120),
    "short":         ("lte", 60),
    "quick":         ("lte", 30),
    "brief":         ("lte", 30),
    "fast":          ("lte", 30),
    "mini":          ("lte", 20),
}

LEVEL_KEYWORDS = {
    "beginner":     ["beginner", "introductory", "introduction", "intro", "foundational", "basic", "101"],
    "intermediate": ["intermediate", "mid", "medium"],
    "advanced":     ["advanced", "expert", "deep dive", "deep-dive"],
}

FORMAT_KEYWORDS = {
    "interactive": ["interactive"],
    "passive":     ["passive"],
    "video":       ["video"],
}

STOPWORDS = {
    "find", "show", "me", "a", "an", "some", "courses", "course", "resource",
    "on", "about", "for", "the", "in", "that", "are", "is", "i", "want",
    "need", "looking", "something", "any", "good", "best", "top", "recommend",
    "please", "can", "you", "minutes", "minute", "min", "hours", "hour",
    "week", "level", "format", "interactive", "passive", "long", "short",
    "quick", "brief", "comprehensive", "beginner", "intermediate", "advanced",
    "under", "over", "less", "than", "more", "with", "and", "or", "have",
    "get", "give", "like",
}


def _norm(s) -> str:
    return str(s).lower().strip() if pd.notna(s) else ""


def _parse_duration_to_mins(raw: str) -> float | None:
    """Convert heterogeneous duration strings → approximate minutes (float)."""
    if not isinstance(raw, str) or not raw.strip():
        return None
    s = raw.lower().strip()

    # patterns: "16 hours", "5 hours a day for 3 days", "12 weeks", "1 year",
    #           "one semester", "35 videos roughly 50 mins each",
    #           "16 videos roughly 4–17 min each", "5hrs", "5hours", "4 hrs"
    patterns = [
        (r"(\d+(?:\.\d+)?)\s*hours?\s*a\s*day\s*for\s*(\d+)\s*days?", lambda m: float(m.group(1)) * int(m.group(2)) * 60),
        (r"(\d+(?:\.\d+)?)\s*hrs?\b", lambda m: float(m.group(1)) * 60),
        (r"(\d+(?:\.\d+)?)\s*hours?\b", lambda m: float(m.group(1)) * 60),
        (r"(\d+)\s*videos?\s*roughly\s*([\d.]+)\s*[-–]\s*([\d.]+)\s*min",
         lambda m: int(m.group(1)) * (float(m.group(2)) + float(m.group(3))) / 2),
        (r"(\d+)\s*videos?\s*roughly\s*([\d.]+)\s*min", lambda m: int(m.group(1)) * float(m.group(2))),
        (r"(\d+(?:\.\d+)?)\s*min(?:s|utes?)?\b", lambda m: float(m.group(1))),
        (r"(\d+)\s*weeks?\b", lambda m: float(m.group(1)) * 5 * 60),     # ~5 hrs/week light estimate
        (r"one\s+semester|a\s+semester", lambda m: 45.0 * 60),
        (r"half\s+a\s+semester", lambda m: 22.5 * 60),
        (r"(\d+)\s*months?\b", lambda m: float(m.group(1)) * 10 * 60),
        (r"(\d+)\s*years?\b", lambda m: float(m.group(1)) * 120 * 60),
    ]
    for pattern, fn in patterns:
        m = re.search(pattern, s)
        if m:
            try:
                return round(fn(m), 1)
            except Exception:
                continue
    
    # Simple float fallback
    try:
        return float(s)
    except ValueError:
        return None

# ─────────────────────────────────────────────────────────────────────────────
def _extract_keywords(question: str) -> list[str]:
    """Use LLM to extract the core search keywords from the user's question."""
    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Extract the core search keywords from the user's course request. "
                        "Return ONLY a JSON array of lowercase strings. No explanation. "
                        "Example: 'find me a beginner python course' → [\"python\"] "
                        "Example: 'NLP and machine learning tutorials' → [\"nlp\", \"natural language processing\", \"machine learning\"] "
                        "Example: 'java programming for beginners' → [\"java\", \"programming\"] "
                        "Include common synonyms or expansions where helpful."
                    ),
                },
                {"role": "user", "content": question},
            ],
            temperature=0,
            max_tokens=100,
        )
        raw = completion.choices[0].message.content.strip()
        clean = re.sub(r"```(?:json)?|```", "", raw).strip()
        keywords = json.loads(clean)
        if isinstance(keywords, list):
            return [str(k).lower().strip() for k in keywords if k]
    except Exception:
        pass

    # Fallback: simple tokenisation
    STOPWORDS_SIMPLE = {
        "find","show","me","a","an","some","courses","course","resource",
        "on","about","for","the","in","that","are","is","i","want","need",
        "looking","something","any","good","best","top","recommend","please",
        "can","you","give","get","like","and","or","with","have","beginner",
        "intermediate","advanced","short","long","quick","under","over",
    }
    return [w for w in re.findall(r'\b\w+\b', question.lower())
            if w not in STOPWORDS_SIMPLE and len(w) > 1]


# ─────────────────────────────────────────────────────────────────────────────
# SMART PRE-FILTER
# ─────────────────────────────────────────────────────────────────────────────
def _pre_filter(question: str, df: pd.DataFrame, max_results: int = 20) -> pd.DataFrame:
    """
    1. Use LLM to extract core keywords from the question.
    2. Search those keywords across key columns.
    3. Return top-scored rows, or full catalogue as fallback.
    """
    # ── Extract keywords via LLM ──────────────────────────────────────────────
    keywords = _extract_keywords(question)
    
    if not keywords:
        return df.head(max_results)

    # ── Columns to search ─────────────────────────────────────────────────────
    search_cols = [c for c in [
    "title", "domain", "focus_area", "full_description",
    "priority_skills", "audience", "short_description",
    "skill_tags", "comments"
] if c in df.columns]
    title_col = "title" if "title" in df.columns else None

    # ── Score each row ────────────────────────────────────────────────────────
    def score_row(row):
     s = 0
     for col in search_cols:
        try:
            cell_text = str(row[col]).lower() if pd.notna(row[col]) else ""
        except Exception:
            cell_text = ""
        for kw in keywords:
            if kw in cell_text:
                s += 3 if col == title_col else 1
     return s

    scores = df.apply(score_row, axis=1)
    matched = df[scores > 0].copy()
    matched["_score"] = scores[scores > 0]
    matched = matched.sort_values("_score", ascending=False).drop(columns=["_score"])

    print(f"[pre_filter] Matched {len(matched)} rows out of {len(df)}")
    print(matched['title'].head(2))
    # ── Fallback to full catalogue if nothing matched ─────────────────────────
    return (matched if not matched.empty else df).head(max_results)

# CATALOGUE CONTEXT
# ─────────────────────────────────────────────────────────────────────────────
def _build_catalogue_context(df: pd.DataFrame) -> str:
    lines = []
    for idx, (_, row) in enumerate(df.iterrows()):
        title_col = _col(df, "title")
        title     = str(row.get(title_col, "Untitled")).strip()
        parts     = [f"COURSE_{idx + 1}: {title}"]
        
        # Iterate through ALL defined columns in COL
        for key, csv_col in COL.items():
            if key == "title": # Already used for the header
                continue
            
            val = row.get(csv_col, "")
            if pd.notna(val) and str(val).strip() not in ("", "nan", "None", "N/A"):
                label = csv_col.upper()
                parts.append(f"  {label}: {str(val).strip()}")
        
        lines.append("\n".join(parts))
    return "\n\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# GROQ CALL
# ─────────────────────────────────────────────────────────────────────────────
_SYSTEM_PROMPT = """You are a course recommendation assistant for a university Student Success platform.

You receive:
1. The student's request (topic, duration, level, format, audience, etc.)
2. A list of courses from the catalogue with detailed fields (description, prerequisites, skills, etc.)

Your task: Select the 3–5 BEST matching courses and return them as a JSON array.

STRICT RULES:
- Only recommend courses explicitly listed in the catalogue context. NEVER invent courses.
- Copy the URL field exactly as given. Do not modify or shorten URLs.
- If a course has no URL (often labelled as 'URL' or 'LMS_LINK'), set "link" to null.
- "duration_display": use the 'LENGTH (MINS)' value. Format it nicely, e.g., "45 mins" or "2 hrs 15 mins". If missing, use "Not Stated".
- "reason": Provide 1-2 concise sentences explaining why this specific course matches the student's request based on the description, skills, or prerequisites provided.
- Be flexible: If an exact match for ALL criteria (e.g., exact level and exact duration) isn't found, pick the closest relevant options and explain why in the "reason".
- Return ONLY a valid JSON array. No markdown fences, no explanation, no preamble.

JSON schema (return exactly this shape):
[
  {
    "title": "Exact Resource title from catalogue",
    "platform": "Platform / host value",
    "level": "Indicated level value or Not Stated",
    "duration_display": "e.g. 45 mins or 2 hrs 30 mins or Not Stated",
    "format": "passive or interactive or Not Stated",
    "captions": "Yes / No / Not Stated",
    "last_updated": "date string or Not Stated",
    "link": "Full URL or null",
    "reason": "Why this fits the student request."
  }
]"""
def _search_courses(question: str, df: pd.DataFrame, history: list) -> dict:
    relevant = _pre_filter(question, df, max_results=20)
    if relevant.empty:
        relevant = df.head(20)

    top3 = relevant.head(3)
    courses = []

    for _, row in top3.iterrows():
        title    = str(row.get("title", "Untitled")).strip()
        url      = str(row.get("lms_link", "")).strip()
        desc     = str(row.get("short_description") or row.get("full_description", "")).strip()
        platform = str(row.get("platform", "")).strip()
        level    = str(row.get("level", "")).strip()
        duration = str(row.get("length_raw", "")).strip()
        fmt      = str(row.get("format", "")).strip()

        courses.append({
            "title":            title,
            "platform":         platform if platform not in ("", "nan") else "Not Stated",
            "level":            level    if level    not in ("", "nan") else "Not Stated",
            "duration_display": duration if duration not in ("", "nan") else "Not Stated",
            "format":           fmt      if fmt      not in ("", "nan") else "Not Stated",
            "captions":         str(row.get("captions", "Not Stated")).strip(),
            "last_updated":     str(row.get("last_updated", "Not Stated")).strip(),
            "link":             url if url not in ("", "nan", "None") else None,
            "reason":           desc[:200] + "..." if len(desc) > 200 else desc,
        })

    count = len(courses)
    noun  = "course" if count == 1 else "courses"
    intro = f"Found {count} {noun} matching your request:" if count else "No matching courses found — try a different search!"

    return {"type": "course_results", "message": intro, "courses": courses}
def _search_courses_old(question: str, df: pd.DataFrame, history: list) -> dict:
    relevant = _pre_filter(question, df, max_results=20)
    if relevant.empty:
        relevant = df.head(20)

    catalogue = _build_catalogue_context(relevant)

    user_msg = (
        f'Student request: "{question}"\n\n'
        f"Available courses (pre-filtered for relevance):\n{catalogue}\n\n"
        "Pick the 3–5 best matches and return them as a JSON array."
    )

    messages = [{"role": "system", "content": _SYSTEM_PROMPT}]
    for m in history:
        role    = m.get("role", "user")
        content = m.get("content", "")
        if isinstance(content, str) and content.strip():
            messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": user_msg})

    completion = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.2,
        max_tokens=1500,
    )

    raw = completion.choices[0].message.content.strip()

    try:
        clean   = re.sub(r"```(?:json)?|```", "", raw).strip()
        courses = json.loads(clean)
        if not isinstance(courses, list):
            raise ValueError("Expected JSON array")

        # ── Fix missing links via lookup ──────────────────────────────────────
        url_col   = _col(df, "lms_link")
        title_col = _col(df, "title")
        link_lookup: dict[str, str] = {}
        if url_col and title_col:
            for _, row in df.iterrows():
                t   = _norm(row.get(title_col, ""))
                lnk = str(row.get(url_col, "")).strip()
                if t and lnk not in ("", "nan", "None"):
                    link_lookup[t] = lnk
        print(courses)
        for course in courses:
            if not course.get("link") or str(course["link"]) in ("null", "nan", "None", ""):
                course["link"] = link_lookup.get(_norm(course.get("title", "")))

        count = len(courses)
        noun  = "course" if count == 1 else "courses"
        intro = (
            f"Found {count} {noun} matching your request:"
            if count else
            "No exact matches found — try broadening your search!"
        )

        return {"type": "course_results", "message": intro, "courses": courses}

    except (json.JSONDecodeError, ValueError):
        return {"type": "text", "content": raw}
# ─────────────────────────────────────────────────────────────────────────────
# INTENT ROUTER — determines if the user wants course search or general chat
# ─────────────────────────────────────────────────────────────────────────────
_ROUTER_PROMPT = """You are an intent classifier for a university Student Success platform.
Your job is to decide if a message is a "course_search" or a "general" conversation.

- "course_search": User wants to find, search, recommend, or filter courses/tutorials. Examples: "find python courses", "NLP tutorials", "beginner data science", "under 5 hours".
- "general": Greetings, thanks, general help, or questions NOT about searching the course catalogue. Examples: "hello", "how are you?", "what is machine learning?", "thanks".

Respond with ONLY the word "course_search" or "general". No punctuation."""


def _classify_intent(question: str, history: list) -> str:
    """Classify user intent as 'course_search' or 'general'."""
    q_lower = question.lower().strip().strip('?!.')
    
    # 1. Immediate Heuristic for Greetings / Politeness
    greetings = {"hi", "hello", "hey", "hola", "greetings", "good morning", "good afternoon", "morning"}
    polite = {"thanks", "thank you", "bye", "goodbye", "help", "who are you"}
    
    if q_lower in greetings or q_lower in polite:
        return "general"

    # 2. Keyword check for obvious course queries
    course_signals = [
        "find", "search", "course", "courses", "learn", "tutorial",
        "recommend", "suggestion", "training", "beginner", "advanced",
        "intermediate", "nlp", "python", "data", "machine learning",
        "interactive", "passive", "duration", "hours", "minutes",
        "thesis", "study", "resource", "platform",
    ]
    signal_count = sum(1 for s in course_signals if s in q_lower)
    if signal_count >= 2:
        return "course_search"

    # 3. LLM Router for everything else

    # For ambiguous cases, ask the LLM
    try:
        messages = [
            {"role": "system", "content": _ROUTER_PROMPT},
            {"role": "user", "content": question}
        ]
        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0,
            max_tokens=10,
        )
        intent = completion.choices[0].message.content.strip().lower()
        return "course_search" if "course" in intent else "general"
    except Exception:
        # Default to general on failure
        return "general"


# ─────────────────────────────────────────────────────────────────────────────
# GENERAL CHAT — handles non-course questions
# ─────────────────────────────────────────────────────────────────────────────
_GENERAL_SYSTEM = """You are a friendly university Student Success assistant. 
You provide warm, concise, and helpful answers to general student questions.

Key duties:
1. Greet the user warmly if they say hi/hello.
2. Answer general educational or university questions (e.g., "what is NLP?").
3. If they seem interested in learning a specific skill, mention that you can also search the course catalogue — they just need to ask for a recommendation!

Be encouraging and professional. Keep responses under 3-4 sentences."""


def _general_chat(question: str, history: list) -> str:
    """Handle general (non-course) questions via LLM."""
    messages = [{"role": "system", "content": _GENERAL_SYSTEM}]
    for m in history:
        role = m.get("role", "user")
        content = m.get("content", "")
        if isinstance(content, str) and content.strip():
            messages.append({"role": role, "content": content})
        elif isinstance(content, dict):
            messages.append({"role": role, "content": content.get("message", "")})
    messages.append({"role": "user", "content": question})

    completion = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=800,
    )
    return completion.choices[0].message.content.strip()


# ─────────────────────────────────────────────────────────────────────────────
# RENDER — Full-page chatbot in the main body area
# ─────────────────────────────────────────────────────────────────────────────
def render_chatbot(df: pd.DataFrame, theme: str = "dark"):
    """Render the course discovery chatbot in the main body area."""

    # Session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    is_dark = theme == "dark"
    bg       = "#0f1117" if is_dark else "#ffffff"
    card_bg  = "#1a1d2e" if is_dark else "#f1f5f9"
    text_c   = "#ffffff" if is_dark else "#1e293b"
    border_c = "#374151" if is_dark else "#e2e8f0"
    accent   = "#6366f1"
    accent2  = "#8b5cf6"

    # ── Custom CSS for chat styling ───────────────────────────────
    st.markdown(f"""
    <style>
    /* Chat message text always white in dark mode */
    .stChatMessage p, .stChatMessage span, .stChatMessage div {{
        color: {text_c} !important;
    }}
    /* Course card styling */
    .course-card {{
        background: {card_bg};
        border: 1px solid {border_c};
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        transition: border-color 0.2s;
    }}
    .course-card:hover {{
        border-color: {accent};
    }}
    .course-card h4 {{
        color: {text_c} !important;
        margin: 0 0 8px 0;
        font-size: 1rem;
    }}
    .course-card .badges {{
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-bottom: 8px;
    }}
    .course-card .badge {{
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
    }}
    .badge-level {{ background: {"#1e3a5f" if is_dark else "#dbeafe"}; color: {"#93c5fd" if is_dark else "#1d4ed8"}; }}
    .badge-duration {{ background: {"#1e2e22" if is_dark else "#dcfce7"}; color: {"#86efac" if is_dark else "#166534"}; }}
    .badge-format {{ background: {"#2d1b4e" if is_dark else "#f3e8ff"}; color: {"#c4b5fd" if is_dark else "#7c3aed"}; }}
    .badge-platform {{ background: {"#1c2538" if is_dark else "#e0f2fe"}; color: {"#7dd3fc" if is_dark else "#0369a1"}; }}
    .course-card .reason {{
        color: {"#94a3b8" if is_dark else "#64748b"};
        font-size: 0.85rem;
        font-style: italic;
        margin: 8px 0;
    }}
    .course-card a {{
        color: {accent};
        text-decoration: none;
        font-weight: 600;
    }}
    .course-card a:hover {{
        color: {accent2};
        text-decoration: underline;
    }}
    </style>
    """, unsafe_allow_html=True)

    # ── Header ────────────────────────────────────────────────────
    col_title, col_clear = st.columns([6, 1])
    with col_title:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:1rem;">
            <span style="font-size:2rem;">🎓</span>
            <div>
                <h2 style="margin:0; color:{text_c};">Student Success Assistant</h2>
                <p style="margin:0; color:#94a3b8; font-size:.85rem;">
                    Ask me anything — or describe a course you're looking for
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_clear:
        if st.button("🗑️ Clear", key="chatbot_clear_btn", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    st.divider()

    # ── Chat History ──────────────────────────────────────────────
    if not st.session_state.chat_history:
        # Empty state
        st.markdown(f"""
        <div style="text-align:center; padding: 3rem 1rem; color:{text_c};">
            <div style="font-size: 3rem; margin-bottom: 1rem;">💬</div>
            <h3 style="color:{text_c}; margin: 0 0 .5rem 0;">Start a conversation</h3>
            <p style="color:#94a3b8; font-size:.9rem; max-width:400px; margin:0 auto;">
                I can help with general questions or find courses for you.<br><br>
                <em>"Hello!"</em> · <em>"What is ML?"</em><br>
                <em>"Find me a long course in NLP"</em><br>
                <em>"Beginner Python, under 60 minutes"</em>
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_history:
            role    = msg["role"]
            mtype   = msg.get("msg_type", "text")
            content = msg.get("content", "")

            if role == "user":
                with st.chat_message("user"):
                    st.markdown(content)
            else:
                with st.chat_message("assistant"):
                    if mtype == "course_results" and isinstance(content, dict):
                        # Show intro text
                        intro = content.get("message", "")
                        if intro:
                            st.markdown(intro)

                        # Show course cards
                        courses = content.get("courses", [])
                        for course in courses:
                            title   = course.get("title", "Untitled")
                            link    = course.get("link")
                            reason  = course.get("reason", "")

                            link_html = f'<a href="{link}" target="_blank">{link}</a>' if link and str(link) not in ("None", "nan", "null", "") else "No link available"

                            st.markdown(f"""
                           <div class="course-card">
                             <p><strong>Title:</strong> {title}</p>
                       <p><strong>URL:</strong> {link_html}</p>
                        <p><strong>Description:</strong> {reason}</p>
                         </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(str(content))

    # ── Chat Input ────────────────────────────────────────────────
    user_input = st.chat_input(
        placeholder="e.g. Find   NLP courses or recommend me  Python under course...",
        key="chatbot_input"
    )

    if user_input and user_input.strip():
        question = user_input.strip()

        # Add user message
        st.session_state.chat_history.append({
            "role": "user",
            "content": question,
            "msg_type": "text"
        })

        # Build LLM history
        llm_history = []
        for m in st.session_state.chat_history[:-1]:
            if isinstance(m.get("content"), str):
                llm_history.append({"role": m["role"], "content": m["content"]})
            elif isinstance(m.get("content"), dict):
                llm_history.append({"role": m["role"], "content": m["content"].get("message", "")})

        # Classify intent: course search or general chat?
        with st.spinner("💭 Thinking..."):
            try:
                intent = _classify_intent(question, llm_history)
            except Exception:
                intent = "general"

        if intent == "course_search":
            # Route to course search agent
            with st.spinner("🔍 Searching courses..."):
                try:
                    result = _search_courses(question, df, llm_history)
                   
                except Exception as e:
                    result = {"type": "text", "content": f"Sorry, I encountered an error: {str(e)}"}

            if result.get("type") == "course_results":
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": result,
                    "msg_type": "course_results"
                })
            else:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": result.get("content", "I couldn't find any matching courses."),
                    "msg_type": "text"
                })
        else:
            # Route to general chat agent
            with st.spinner("💬 Responding..."):
                try:
                    response = _general_chat(question, llm_history)
                except Exception as e:
                    response = f"Sorry, I encountered an error: {str(e)}"

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response,
                "msg_type": "text"
            })

        st.rerun()
