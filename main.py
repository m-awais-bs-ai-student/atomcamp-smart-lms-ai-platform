import streamlit as st
import google.generativeai as genai
import json
import time
import random
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from anthropic import Anthropic
import os

genai.configure(api_key="AIzaSyAt2ioiH1dhathyDcAaWwlcyMHsg58lO_A")

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="atomcamp · Smart LMS",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS Styling ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --atom-bg: #0a0e1a;
    --atom-surface: #111827;
    --atom-card: #1a2235;
    --atom-border: #2d3748;
    --atom-accent: #00d4ff;
    --atom-green: #00ff88;
    --atom-orange: #ff6b35;
    --atom-purple: #8b5cf6;
    --atom-text: #e2e8f0;
    --atom-muted: #94a3b8;
}

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
}

.stApp { background: var(--atom-bg) !important; }

.main-header {
    background: linear-gradient(135deg, #0a0e1a 0%, #1a0a2e 50%, #0a1a2e 100%);
    border-bottom: 1px solid var(--atom-border);
    padding: 1.5rem 2rem;
    margin: -1rem -1rem 2rem -1rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.atom-logo {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #00d4ff, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
}

.metric-card {
    background: var(--atom-card);
    border: 1px solid var(--atom-border);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
}

.metric-card:hover {
    border-color: var(--atom-accent);
    transform: translateY(-2px);
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    color: var(--atom-accent);
}

.metric-label {
    color: var(--atom-muted);
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.course-card {
    background: var(--atom-card);
    border: 1px solid var(--atom-border);
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    cursor: pointer;
    transition: all 0.2s ease;
}

.course-card:hover {
    border-color: var(--atom-accent);
    background: #1f2d45;
}

.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.badge-ai { background: #1a1040; color: #8b5cf6; border: 1px solid #8b5cf6; }
.badge-data { background: #001a30; color: #00d4ff; border: 1px solid #00d4ff; }
.badge-boot { background: #1a2a00; color: #00ff88; border: 1px solid #00ff88; }
.badge-hot { background: #2a0a00; color: #ff6b35; border: 1px solid #ff6b35; }

.ai-chat-bubble {
    background: linear-gradient(135deg, #1a2235, #1a1040);
    border: 1px solid #8b5cf6;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
    color: var(--atom-text);
}

.user-chat-bubble {
    background: linear-gradient(135deg, #001a30, #001a20);
    border: 1px solid #00d4ff;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
    color: var(--atom-text);
}

.progress-bar-bg {
    background: var(--atom-border);
    border-radius: 8px;
    height: 8px;
    overflow: hidden;
}

.progress-bar-fill {
    height: 100%;
    border-radius: 8px;
    background: linear-gradient(90deg, #00d4ff, #8b5cf6);
    transition: width 0.5s ease;
}

.insight-card {
    background: linear-gradient(135deg, #0a1a0a, #001a10);
    border: 1px solid #00ff88;
    border-radius: 12px;
    padding: 1rem;
    margin: 0.5rem 0;
}

.warning-card {
    background: linear-gradient(135deg, #1a0a00, #2a1000);
    border: 1px solid #ff6b35;
    border-radius: 12px;
    padding: 1rem;
    margin: 0.5rem 0;
}

.section-title {
    font-size: 1.4rem;
    font-weight: 600;
    color: var(--atom-text);
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--atom-border);
}

.stButton > button {
    background: linear-gradient(135deg, #00d4ff20, #8b5cf620) !important;
    border: 1px solid #00d4ff !important;
    color: #00d4ff !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #00d4ff40, #8b5cf640) !important;
    transform: translateY(-1px) !important;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background: var(--atom-card) !important;
    border: 1px solid var(--atom-border) !important;
    color: var(--atom-text) !important;
    border-radius: 8px !important;
}

.stSidebar {
    background: var(--atom-surface) !important;
}

[data-testid="stSidebar"] {
    background: var(--atom-surface) !important;
    border-right: 1px solid var(--atom-border) !important;
}

.sidebar-nav-item {
    padding: 0.6rem 1rem;
    border-radius: 8px;
    cursor: pointer;
    color: var(--atom-muted);
    transition: all 0.2s;
    margin: 2px 0;
}

.sidebar-nav-item:hover {
    background: var(--atom-card);
    color: var(--atom-accent);
}

.quiz-option {
    background: var(--atom-card);
    border: 1px solid var(--atom-border);
    border-radius: 8px;
    padding: 0.8rem 1rem;
    cursor: pointer;
    margin: 0.4rem 0;
    transition: all 0.2s;
}

.stRadio > div { color: var(--atom-text) !important; }
.stMarkdown, .stText { color: var(--atom-text) !important; }
h1, h2, h3, h4, h5, h6 { color: var(--atom-text) !important; }
p { color: var(--atom-text) !important; }
label { color: var(--atom-muted) !important; }

.pulse-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--atom-green);
    animation: pulse 2s infinite;
    margin-right: 6px;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.3); }
}
</style>
""", unsafe_allow_html=True)

# ─── Initialize State ──────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "page": "dashboard",
        "onboarded": False,
        "learner": {},
        "chat_history": [],
        "quiz_state": {"active": False, "questions": [], "current": 0, "score": 0, "answers": []},
        "enrolled_courses": [],
        "progress": {},
        "notifications": [],
        "xp_points": 0,
        "streak_days": 0,
        "last_activity": None,
        "learning_path": [],
        "instructor_view": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─── Data ──────────────────────────────────────────────────────────────────────
COURSES = {
    "ai_bootcamp": {
        "id": "ai_bootcamp", "title": "AI Bootcamp", "category": "AI",
        "duration": "2 months", "level": "Intermediate",
        "description": "Hands-on AI agent building program with live expert guidance.",
        "modules": ["Python for AI", "ML Fundamentals", "Deep Learning", "NLP Basics", "AI Agents", "Capstone Project"],
        "enrolled": 1240, "rating": 4.8, "badge": "badge-ai", "xp": 500,
        "skills": ["Python", "TensorFlow", "LangChain", "Prompt Engineering"]
    },
    "data_analytics": {
        "id": "data_analytics", "title": "Data Analytics Bootcamp", "category": "Data",
        "duration": "2 months", "level": "Beginner",
        "description": "Industry-aligned data analytics program with real-world projects.",
        "modules": ["Excel & SQL", "Python Basics", "Data Viz", "Statistics", "Dashboards", "Capstone"],
        "enrolled": 980, "rating": 4.7, "badge": "badge-data", "xp": 400,
        "skills": ["Python", "SQL", "Power BI", "Tableau", "Statistics"]
    },
    "agentic_ai": {
        "id": "agentic_ai", "title": "Agentic AI", "category": "AI",
        "duration": "3 months", "level": "Advanced",
        "description": "Build autonomous AI agents and multi-agent workflows.",
        "modules": ["LLM Architecture", "Tool Use & MCP", "Agent Frameworks", "RAG Systems", "Production Deploy", "Capstone"],
        "enrolled": 430, "rating": 4.9, "badge": "badge-hot", "xp": 600,
        "skills": ["LangGraph", "CrewAI", "RAG", "Vector DBs", "APIs"]
    },
    "automation": {
        "id": "automation", "title": "AI Automation", "category": "AI",
        "duration": "6 weeks", "level": "Beginner",
        "description": "Automate workflows using AI tools and no-code platforms.",
        "modules": ["n8n Basics", "Zapier & Make", "AI APIs", "RPA Intro", "Business Automation"],
        "enrolled": 670, "rating": 4.6, "badge": "badge-boot", "xp": 300,
        "skills": ["n8n", "Zapier", "Make.com", "Python", "APIs"]
    }
}

LEARNER_PROFILES = {
    "beginner": {"xp_mult": 1.0, "recommend": ["data_analytics", "automation"]},
    "intermediate": {"xp_mult": 1.2, "recommend": ["ai_bootcamp", "data_analytics"]},
    "advanced": {"xp_mult": 1.5, "recommend": ["agentic_ai", "ai_bootcamp"]},
}

# client = Anthropic()

# ─── AI Helpers ────────────────────────────────────────────────────────────────
def get_ai_response(system_prompt: str, user_message: str, history: list = None) -> str:
    try:
        model = genai.GenerativeModel("gemini-3-flash-preview")

        chat = model.start_chat(history=[])

        full_prompt = system_prompt + "\n\nUser: " + user_message

        response = chat.send_message(full_prompt)

        return response.text

    except Exception as e:
        return f"⚠️ AI unavailable: {str(e)[:100]}"

def generate_quiz(topic: str, level: str) -> list:
    prompt = f"""Generate 5 multiple-choice quiz questions about "{topic}" for {level} level learners.
Return ONLY valid JSON array like:
[{{"question":"...","options":["A","B","C","D"],"correct":0,"explanation":"..."}}]
No markdown, no extra text."""
    try:
        resp = get_ai_response("You are an expert quiz generator. Return only JSON.", prompt)
        resp = resp.strip().replace("```json","").replace("```","").strip()
        return json.loads(resp)
    except:
        return [
            {"question": f"What is a key concept in {topic}?",
             "options": ["Machine Learning", "Data Cleaning", "Visualization", "All of above"],
             "correct": 3, "explanation": f"All are core to {topic}."}
        ]

def analyze_learner_performance(learner: dict, progress: dict) -> str:
    summary = json.dumps({"learner": learner, "progress": progress}, indent=2)
    return get_ai_response(
        "You are an adaptive learning coach at atomcamp. Analyze performance and give 3 specific, actionable insights. Be concise and encouraging. Use bullet points.",
        f"Analyze this learner's data:\n{summary}"
    )

def generate_learning_path(learner: dict) -> str:
    return get_ai_response(
        "You are atomcamp's AI curriculum advisor. Create a personalized 8-week learning path. Be specific with week-by-week breakdown.",
        f"Create a personalized learning path for: {json.dumps(learner)}"
    )

# ─── Sidebar ───────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="atom-logo">⚛ atomcamp</div>', unsafe_allow_html=True)
        st.markdown('<div style="color:#94a3b8; font-size:0.8rem; margin-bottom:1.5rem;">Smart Adaptive LMS</div>', unsafe_allow_html=True)

        if st.session_state.onboarded:
            learner = st.session_state.learner
            xp = st.session_state.xp_points
            st.markdown(f"""
            <div style="background:#1a2235;border:1px solid #2d3748;border-radius:12px;padding:1rem;margin-bottom:1rem;">
                <div style="font-weight:600;color:#e2e8f0;">👤 {learner.get('name','Learner')}</div>
                <div style="color:#94a3b8;font-size:0.8rem;">{learner.get('level','Beginner')} · {learner.get('goal','')}</div>
                <div style="margin-top:0.8rem;">
                    <div style="color:#00d4ff;font-family:'JetBrains Mono';font-size:1.2rem;font-weight:700;">{xp} XP</div>
                    <div style="color:#94a3b8;font-size:0.75rem;">🔥 {st.session_state.streak_days} day streak</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("**Navigation**")
        pages = [
            ("🏠", "dashboard", "Dashboard"),
            ("🎯", "onboarding", "Create Profile"),
            ("📚", "courses", "Courses"),
            ("🤖", "ai_tutor", "AI Tutor"),
            ("📝", "quiz", "Smart Quiz"),
            ("📊", "analytics", "Analytics"),
            ("🗺️", "learning_path", "Learning Path"),
            ("👨‍🏫", "instructor", "Instructor View"),
        ]
        for icon, page_id, label in pages:
            active = "border-left: 2px solid #00d4ff; color:#00d4ff;" if st.session_state.page == page_id else ""
            if st.button(f"{icon} {label}", key=f"nav_{page_id}", use_container_width=True):
                st.session_state.page = page_id
                st.rerun()

        st.markdown("---")
        st.markdown(f'<div style="color:#94a3b8;font-size:0.75rem;"><span class="pulse-dot"></span>AI-Powered · Live</div>', unsafe_allow_html=True)

# ─── Pages ─────────────────────────────────────────────────────────────────────

def page_dashboard():
    st.markdown("## 🏠 Dashboard")

    if not st.session_state.onboarded:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#0a0e1a,#1a0a2e);border:1px solid #8b5cf6;border-radius:16px;padding:2rem;text-align:center;margin-bottom:2rem;">
            <div style="font-size:3rem;">⚛️</div>
            <h2 style="color:#e2e8f0;margin:0.5rem 0;">Welcome to atomcamp Smart LMS</h2>
            <p style="color:#94a3b8;">Pakistan's most intelligent adaptive learning platform. Let's personalize your journey.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Start Onboarding →", use_container_width=True):
            st.session_state.page = "onboarding"
            st.rerun()
        return

    learner = st.session_state.learner
    enrolled = st.session_state.enrolled_courses
    progress = st.session_state.progress

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-value">{st.session_state.xp_points}</div>
            <div class="metric-label">XP Points</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-value">{len(enrolled)}</div>
            <div class="metric-label">Enrolled</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        avg_prog = int(np.mean([progress.get(c, 0) for c in enrolled])) if enrolled else 0
        st.markdown(f"""<div class="metric-card">
            <div class="metric-value">{avg_prog}%</div>
            <div class="metric-label">Avg Progress</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-value">{st.session_state.streak_days}🔥</div>
            <div class="metric-label">Day Streak</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown("### 📚 My Courses")
        if not enrolled:
            st.info("You haven't enrolled in any courses yet. Visit the Courses page!")
        for cid in enrolled:
            c = COURSES.get(cid, {})
            prog = progress.get(cid, 0)
            st.markdown(f"""
            <div class="course-card">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span class="badge {c.get('badge','badge-ai')}">{c.get('category','AI')}</span>
                        <span style="font-weight:600;color:#e2e8f0;margin-left:0.5rem;">{c.get('title','')}</span>
                    </div>
                    <span style="color:#00d4ff;font-family:'JetBrains Mono';">{prog}%</span>
                </div>
                <div class="progress-bar-bg" style="margin-top:0.8rem;">
                    <div class="progress-bar-fill" style="width:{prog}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Continue Learning →", key=f"cont_{cid}"):
                st.session_state.page = "courses"
                st.rerun()

    with col_right:
        st.markdown("### 🔔 AI Insights")
        if enrolled and progress:
            with st.spinner("Analyzing your progress..."):
                insights = analyze_learner_performance(learner, progress)
            st.markdown(f'<div class="insight-card">{insights}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="insight-card">📡 Enroll in a course to get personalized AI insights!</div>', unsafe_allow_html=True)

        st.markdown("### 🏆 Next Milestone")
        next_xp = ((st.session_state.xp_points // 100) + 1) * 100
        prog_to_next = int((st.session_state.xp_points % 100))
        st.markdown(f"""
        <div class="metric-card">
            <div style="color:#94a3b8;font-size:0.8rem;">Progress to {next_xp} XP</div>
            <div class="progress-bar-bg" style="margin:0.5rem 0;">
                <div class="progress-bar-fill" style="width:{prog_to_next}%;"></div>
            </div>
            <div style="color:#00d4ff;font-family:'JetBrains Mono';">{st.session_state.xp_points} / {next_xp}</div>
        </div>
        """, unsafe_allow_html=True)


def page_onboarding():
    st.markdown("## 🎯 Learner Onboarding")
    st.markdown('<p style="color:#94a3b8;">Help us personalize your atomcamp experience.</p>', unsafe_allow_html=True)

    with st.form("onboarding_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", placeholder="e.g. Aisha Khan")
            level = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced"])
            background = st.selectbox("Professional Background", [
                "Student", "Software Engineer", "Data Analyst", "Business Professional",
                "Researcher", "Educator", "Healthcare", "Other"
            ])
        with col2:
            goal = st.selectbox("Primary Learning Goal", [
                "Get a job in AI/Data", "Upskill in current role",
                "Build AI projects", "Start a tech business", "Academic research"
            ])
            hours_per_week = st.slider("Hours available per week", 2, 20, 8)
            learning_style = st.selectbox("Preferred Learning Style", [
                "Hands-on Projects", "Video Lectures", "Reading & Theory",
                "Live Sessions", "Mixed Approach"
            ])

        interests = st.multiselect("Topics of Interest", [
            "Machine Learning", "Data Analytics", "AI Agents", "NLP",
            "Computer Vision", "Automation", "Business Intelligence", "GenAI"
        ])

        submitted = st.form_submit_button("✨ Generate My Personalized Profile", use_container_width=True)

    if submitted and name:
        learner = {
            "name": name, "level": level, "background": background,
            "goal": goal, "hours_per_week": hours_per_week,
            "learning_style": learning_style, "interests": interests,
            "joined": datetime.now().strftime("%Y-%m-%d")
        }
        st.session_state.learner = learner
        st.session_state.onboarded = True
        st.session_state.xp_points = 50
        st.session_state.streak_days = 1

        # AI-generated welcome
        with st.spinner("🤖 AI is personalizing your profile..."):
            welcome = get_ai_response(
                "You are atomcamp's onboarding AI. Give a warm, personalized 3-sentence welcome message with 2 specific course recommendations based on their profile. Be concise and motivating.",
                f"New learner profile: {json.dumps(learner)}"
            )

        st.balloons()
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0a1a0a,#001a10);border:1px solid #00ff88;border-radius:16px;padding:1.5rem;margin-top:1rem;">
            <div style="color:#00ff88;font-size:1.1rem;font-weight:600;margin-bottom:0.5rem;">✅ Profile Created!</div>
            <div style="color:#e2e8f0;">{welcome}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Go to Dashboard →"):
            st.session_state.page = "dashboard"
            st.rerun()


def page_courses():
    st.markdown("## 📚 Course Catalogue")

    col_filter, col_search = st.columns([1, 3])
    with col_filter:
        cat_filter = st.selectbox("Category", ["All", "AI", "Data", "Automation"])
    with col_search:
        search = st.text_input("🔍 Search courses", placeholder="e.g. machine learning, python...")

    # Personalized recommendation banner
    if st.session_state.onboarded:
        level = st.session_state.learner.get("level", "Beginner").lower()
        rec_ids = LEARNER_PROFILES.get(level, LEARNER_PROFILES["beginner"])["recommend"]
        rec_names = [COURSES[r]["title"] for r in rec_ids if r in COURSES]
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#001a30,#0a0020);border:1px solid #00d4ff;border-radius:12px;padding:1rem;margin-bottom:1rem;">
            🤖 <span style="color:#00d4ff;font-weight:600;">AI Recommends:</span>
            <span style="color:#e2e8f0;"> Based on your {level} level — try <strong>{' & '.join(rec_names)}</strong></span>
        </div>
        """, unsafe_allow_html=True)

    for cid, course in COURSES.items():
        if cat_filter != "All" and course["category"] != cat_filter:
            continue
        if search and search.lower() not in course["title"].lower() and search.lower() not in course["description"].lower():
            continue

        enrolled = cid in st.session_state.enrolled_courses
        prog = st.session_state.progress.get(cid, 0)

        with st.expander(f"{'✅' if enrolled else '📖'} {course['title']} — {course['duration']} · {course['level']}", expanded=False):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f'<span class="badge {course["badge"]}">{course["category"]}</span>', unsafe_allow_html=True)
                st.write(course["description"])
                st.markdown("**Modules:**")
                for i, mod in enumerate(course["modules"]):
                    st.markdown(f"- {'✅' if enrolled and (i / len(course['modules'])) * 100 < prog else '📝'} {mod}")
                st.markdown(f"**Skills you'll gain:** {', '.join(course['skills'])}")
            with col2:
                st.metric("⭐ Rating", course["rating"])
                st.metric("👥 Enrolled", f"{course['enrolled']:,}")
                st.metric("🏆 XP", course["xp"])

                if not enrolled:
                    if st.button("Enroll Now", key=f"enroll_{cid}", use_container_width=True):
                        st.session_state.enrolled_courses.append(cid)
                        st.session_state.progress[cid] = 0
                        st.session_state.xp_points += 20
                        st.success(f"Enrolled in {course['title']}! +20 XP")
                        st.rerun()
                else:
                    st.markdown(f'<div style="color:#00ff88;font-weight:600;">✅ Enrolled ({prog}%)</div>', unsafe_allow_html=True)
                    new_prog = st.slider("Simulate Progress", 0, 100, prog, key=f"prog_{cid}")
                    if new_prog != prog:
                        xp_gain = int((new_prog - prog) * course["xp"] / 100)
                        st.session_state.progress[cid] = new_prog
                        st.session_state.xp_points += max(0, xp_gain)
                        st.session_state.streak_days += 1
                        st.rerun()


def page_ai_tutor():
    st.markdown("## 🤖 AI Learning Tutor")
    st.markdown('<p style="color:#94a3b8;">Ask anything about your courses, career, or learning strategy.</p>', unsafe_allow_html=True)

    system_prompt = f"""You are AtomBot, atomcamp's intelligent AI learning tutor. atomcamp is Pakistan's leading AI & data education platform offering bootcamps in AI, Data Analytics, Agentic AI, and Automation.

Learner profile: {json.dumps(st.session_state.learner) if st.session_state.learner else 'Not yet onboarded'}
Enrolled courses: {st.session_state.enrolled_courses}
Progress: {st.session_state.progress}

Your role:
- Help learners understand course concepts
- Answer technical questions about AI, data, Python, ML
- Provide motivation and study strategies
- Suggest resources and next steps
- Be friendly, culturally sensitive, and encouraging
- Keep responses focused and practical"""

    # Chat history display
    chat_container = st.container()
    with chat_container:
        if not st.session_state.chat_history:
            st.markdown("""
            <div class="ai-chat-bubble">
                <strong>🤖 AtomBot:</strong> Assalamu Alaikum! I'm AtomBot, your personal AI tutor at atomcamp. 
                I can help you with course concepts, career advice, technical questions, and more. 
                What would you like to learn today? 🚀
            </div>
            """, unsafe_allow_html=True)

        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-chat-bubble"><strong>👤 You:</strong> {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="ai-chat-bubble"><strong>🤖 AtomBot:</strong> {msg["content"]}</div>', unsafe_allow_html=True)

    # Quick prompts
    st.markdown("**💡 Quick Prompts:**")
    qcol1, qcol2, qcol3 = st.columns(3)
    quick_prompts = [
        "Explain neural networks simply",
        "How do I start with Python?",
        "What career paths suit a data analyst?",
        "Explain RAG in AI agents",
        "Tips for staying motivated",
        "Difference between ML and AI?",
    ]
    for i, qp in enumerate(quick_prompts):
        col = [qcol1, qcol2, qcol3][i % 3]
        with col:
            if st.button(qp, key=f"qp_{i}", use_container_width=True):
                with st.spinner("AtomBot is thinking..."):
                    resp = get_ai_response(system_prompt, qp, st.session_state.chat_history)
                st.session_state.chat_history.append({"role": "user", "content": qp})
                st.session_state.chat_history.append({"role": "assistant", "content": resp})
                st.session_state.xp_points += 5
                st.rerun()

    # Input
    user_input = st.chat_input("Ask AtomBot anything...")
    if user_input:
        with st.spinner("🤖 AtomBot is thinking..."):
            resp = get_ai_response(system_prompt, user_input, st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": resp})
        st.session_state.xp_points += 5
        st.rerun()

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()


def page_quiz():
    st.markdown("## 📝 Adaptive Smart Quiz")
    st.markdown('<p style="color:#94a3b8;">AI-generated quizzes that adapt to your knowledge level.</p>', unsafe_allow_html=True)

    qs = st.session_state.quiz_state

    if not qs["active"]:
        col1, col2 = st.columns(2)
        with col1:
            topic = st.selectbox("Quiz Topic", [
                "Python Basics", "Machine Learning", "Data Analytics",
                "AI Agents", "Neural Networks", "SQL", "Statistics",
                "Natural Language Processing", "Deep Learning"
            ])
        with col2:
            level = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])

        if st.button("🎯 Generate Adaptive Quiz", use_container_width=True):
            with st.spinner("🤖 AI is crafting personalized questions..."):
                questions = generate_quiz(topic, level)
            st.session_state.quiz_state = {
                "active": True, "questions": questions, "current": 0,
                "score": 0, "answers": [], "topic": topic, "level": level
            }
            st.rerun()

    else:
        questions = qs["questions"]
        current = qs["current"]

        if current < len(questions):
            q = questions[current]
            st.markdown(f"""
            <div style="background:#1a2235;border:1px solid #2d3748;border-radius:12px;padding:1.5rem;margin-bottom:1rem;">
                <div style="color:#94a3b8;font-size:0.8rem;text-transform:uppercase;letter-spacing:1px;">
                    Question {current + 1} of {len(questions)} · {qs.get('topic','')} · {qs.get('level','')}
                </div>
                <div style="color:#e2e8f0;font-size:1.1rem;font-weight:600;margin-top:0.5rem;">{q['question']}</div>
            </div>
            """, unsafe_allow_html=True)

            answer = st.radio("Select your answer:", q["options"], key=f"q_{current}")
            selected_idx = q["options"].index(answer)

            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("Submit Answer →", use_container_width=True):
                    is_correct = selected_idx == q["correct"]
                    qs["answers"].append({"question": q["question"], "selected": selected_idx,
                                          "correct": q["correct"], "is_correct": is_correct})
                    if is_correct:
                        qs["score"] += 1
                        st.success(f"✅ Correct! +10 XP  — {q['explanation']}")
                        st.session_state.xp_points += 10
                    else:
                        st.error(f"❌ Incorrect. The answer was: {q['options'][q['correct']]}  — {q['explanation']}")

                    time.sleep(0.5)
                    qs["current"] += 1
                    st.session_state.quiz_state = qs
                    st.rerun()

            # Progress bar
            prog = int((current / len(questions)) * 100)
            st.markdown(f"""
            <div class="progress-bar-bg" style="margin-top:1rem;">
                <div class="progress-bar-fill" style="width:{prog}%;"></div>
            </div>
            """, unsafe_allow_html=True)

        else:
            # Results
            score = qs["score"]
            total = len(questions)
            pct = int((score / total) * 100) if total else 0
            xp_earned = score * 10

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0a1a0a,#001a10);border:1px solid #00ff88;border-radius:16px;padding:2rem;text-align:center;margin-bottom:1.5rem;">
                <div style="font-size:3rem;">{'🏆' if pct >= 80 else '📚' if pct >= 60 else '💪'}</div>
                <div style="color:#00ff88;font-size:1.5rem;font-weight:700;">{pct}% Score</div>
                <div style="color:#e2e8f0;">{score}/{total} correct · +{xp_earned} XP earned</div>
            </div>
            """, unsafe_allow_html=True)

            # AI Feedback
            with st.spinner("Getting personalized feedback..."):
                feedback = get_ai_response(
                    "You are an adaptive learning coach. Give specific feedback on quiz performance.",
                    f"Quiz results: {score}/{total} on {qs.get('topic')} at {qs.get('level')} level. Wrong answers: {[a for a in qs['answers'] if not a['is_correct']]}"
                )
            st.markdown(f'<div class="ai-chat-bubble">🤖 <strong>AI Feedback:</strong> {feedback}</div>', unsafe_allow_html=True)

            if st.button("🔄 New Quiz", use_container_width=True):
                st.session_state.quiz_state = {"active": False, "questions": [], "current": 0, "score": 0, "answers": []}
                st.rerun()


def page_analytics():
    st.markdown("## 📊 Learning Analytics")

    if not st.session_state.onboarded:
        st.info("Complete onboarding to see your analytics.")
        return

    enrolled = st.session_state.enrolled_courses
    progress = st.session_state.progress

    tab1, tab2, tab3 = st.tabs(["📈 Progress", "⏱️ Activity", "🧠 Skill Map"])

    with tab1:
        if enrolled:
            courses_data = [COURSES[c]["title"] for c in enrolled if c in COURSES]
            prog_data = [progress.get(c, 0) for c in enrolled if c in COURSES]

            fig = go.Figure(go.Bar(
                x=prog_data, y=courses_data, orientation='h',
                marker=dict(color=['#00d4ff', '#8b5cf6', '#00ff88', '#ff6b35'][:len(prog_data)],
                            line=dict(color='rgba(0,0,0,0)', width=0)),
                text=[f"{p}%" for p in prog_data], textposition='outside',
                textfont=dict(color='#e2e8f0')
            ))
            fig.update_layout(
                title="Course Progress", paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(26,34,53,0.8)', font=dict(color='#e2e8f0', family='Space Grotesk'),
                xaxis=dict(range=[0, 120], gridcolor='#2d3748', color='#94a3b8'),
                yaxis=dict(gridcolor='#2d3748', color='#94a3b8'),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Enroll in courses to see progress analytics.")

    with tab2:
        # Simulated activity heatmap
        dates = pd.date_range(end=datetime.now(), periods=30)
        activity = np.random.randint(0, 5, 30)
        activity[-3:] = [2, 3, 4]  # Recent activity

        fig2 = go.Figure(go.Scatter(
            x=list(dates), y=list(activity),
            mode='lines+markers',
            line=dict(color='#00d4ff', width=2),
            marker=dict(size=6, color='#8b5cf6'),
            fill='tozeroy', fillcolor='rgba(0,212,255,0.1)'
        ))
        fig2.update_layout(
            title="Learning Activity (Last 30 Days)", paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(26,34,53,0.8)', font=dict(color='#e2e8f0', family='Space Grotesk'),
            xaxis=dict(gridcolor='#2d3748', color='#94a3b8'),
            yaxis=dict(gridcolor='#2d3748', color='#94a3b8', title='Sessions'),
            height=280
        )
        st.plotly_chart(fig2, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Total Sessions", "23", "+3 this week")
        with col2: st.metric("Avg Session", "45 min", "+5 min")
        with col3: st.metric("Best Streak", f"{max(st.session_state.streak_days, 3)} days", "🔥")

    with tab3:
        skills = ["Python", "Machine Learning", "Data Viz", "Statistics", "SQL", "AI Tools", "Communication"]
        values = [75, 60, 80, 55, 70, 65, 85]

        fig3 = go.Figure(go.Scatterpolar(
            r=values + [values[0]], theta=skills + [skills[0]],
            fill='toself', fillcolor='rgba(139,92,246,0.2)',
            line=dict(color='#8b5cf6', width=2),
            marker=dict(color='#00d4ff', size=8)
        ))
        fig3.update_layout(
            polar=dict(bgcolor='rgba(26,34,53,0.8)',
                       radialaxis=dict(gridcolor='#2d3748', color='#94a3b8', range=[0, 100]),
                       angularaxis=dict(gridcolor='#2d3748', color='#e2e8f0')),
            paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0', family='Space Grotesk'),
            title="Skill Radar Chart", height=400
        )
        st.plotly_chart(fig3, use_container_width=True)


def page_learning_path():
    st.markdown("## 🗺️ AI-Generated Learning Path")
    st.markdown('<p style="color:#94a3b8;">Your personalized roadmap to achieving your learning goals.</p>', unsafe_allow_html=True)

    if not st.session_state.onboarded:
        st.warning("Please complete onboarding first to generate your learning path.")
        return

    if st.button("🤖 Generate / Refresh My Learning Path", use_container_width=True):
        with st.spinner("AI is crafting your personalized learning roadmap..."):
            path = generate_learning_path(st.session_state.learner)
        st.session_state.learning_path = path
        st.session_state.xp_points += 15

    if st.session_state.learning_path:
        st.markdown(f"""
        <div class="ai-chat-bubble">
            <strong>🗺️ Your AI Learning Path:</strong><br><br>
            {st.session_state.learning_path.replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)

    # Visual milestone timeline
    st.markdown("### 📍 Milestone Timeline")
    milestones = [
        {"week": "Week 1-2", "title": "Foundation", "desc": "Python basics + data types", "color": "#00d4ff"},
        {"week": "Week 3-4", "title": "Core Skills", "desc": "ML concepts + first models", "color": "#8b5cf6"},
        {"week": "Week 5-6", "title": "Applied", "desc": "Real datasets + projects", "color": "#00ff88"},
        {"week": "Week 7-8", "title": "Capstone", "desc": "Portfolio project + review", "color": "#ff6b35"},
    ]

    cols = st.columns(4)
    for i, (col, ms) in enumerate(zip(cols, milestones)):
        with col:
            st.markdown(f"""
            <div style="background:#1a2235;border:1px solid {ms['color']};border-radius:12px;padding:1rem;text-align:center;">
                <div style="color:{ms['color']};font-size:0.75rem;font-weight:700;text-transform:uppercase;">{ms['week']}</div>
                <div style="color:#e2e8f0;font-weight:600;margin:0.3rem 0;">{ms['title']}</div>
                <div style="color:#94a3b8;font-size:0.8rem;">{ms['desc']}</div>
            </div>
            """, unsafe_allow_html=True)


def page_instructor():
    st.markdown("## 👨‍🏫 Instructor Dashboard")
    st.markdown('<p style="color:#94a3b8;">Real-time learner intelligence for instructors and admins.</p>', unsafe_allow_html=True)

    # Cohort Overview
    col1, col2, col3, col4 = st.columns(4)
    metrics = [("Total Learners", "1,240", "+12%"), ("Avg Completion", "67%", "+5%"),
               ("At-Risk Learners", "23", "-3"), ("Avg Quiz Score", "74%", "+2%")]
    for col, (label, val, delta) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.metric(label, val, delta)

    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["📊 Cohort Analytics", "⚠️ At-Risk Alerts", "💡 AI Recommendations"])

    with tab1:
        # Engagement distribution
        labels = ["Highly Engaged", "On Track", "At Risk", "Inactive"]
        values = [420, 580, 160, 80]
        colors = ['#00ff88', '#00d4ff', '#ff6b35', '#ef4444']

        fig = go.Figure(go.Pie(
            labels=labels, values=values,
            marker=dict(colors=colors, line=dict(color='#0a0e1a', width=2)),
            textfont=dict(color='#e2e8f0'), hole=0.4
        ))
        fig.update_layout(
            title="Learner Engagement Distribution", paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', family='Space Grotesk'),
            legend=dict(font=dict(color='#e2e8f0')), height=350
        )
        st.plotly_chart(fig, use_container_width=True)

        # Module completion heatmap
        modules = ["Intro", "Python", "ML Basics", "Projects", "Advanced"]
        cohorts = ["Cohort 24", "Cohort 25", "Cohort 26"]
        completion_data = [[92, 85, 78, 65, 54], [88, 80, 72, 60, 48], [95, 90, 82, 70, 58]]

        fig2 = go.Figure(go.Heatmap(
            z=completion_data, x=modules, y=cohorts,
            colorscale=[[0, '#1a2235'], [0.5, '#8b5cf6'], [1, '#00d4ff']],
            text=[[f"{v}%" for v in row] for row in completion_data],
            texttemplate="%{text}", textfont=dict(color='white')
        ))
        fig2.update_layout(
            title="Module Completion by Cohort (%)", paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(26,34,53,0.8)', font=dict(color='#e2e8f0', family='Space Grotesk'),
            height=250
        )
        st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        at_risk = [
            {"name": "Ali Hassan", "course": "AI Bootcamp", "last_active": "8 days ago", "progress": 23, "risk": "High"},
            {"name": "Sara Malik", "course": "Data Analytics", "last_active": "5 days ago", "progress": 38, "risk": "Medium"},
            {"name": "Omar Farooq", "course": "AI Bootcamp", "last_active": "12 days ago", "progress": 15, "risk": "High"},
        ]

        for learner in at_risk:
            color = "#ef4444" if learner["risk"] == "High" else "#ff6b35"
            st.markdown(f"""
            <div class="warning-card">
                <div style="display:flex;justify-content:space-between;">
                    <div>
                        <span style="color:#e2e8f0;font-weight:600;">{learner['name']}</span>
                        <span style="color:#94a3b8;margin-left:0.5rem;">· {learner['course']}</span>
                    </div>
                    <span style="color:{color};font-weight:700;">{learner['risk']} Risk</span>
                </div>
                <div style="color:#94a3b8;font-size:0.85rem;margin-top:0.3rem;">
                    Last active: {learner['last_active']} · Progress: {learner['progress']}%
                </div>
                <div class="progress-bar-bg" style="margin-top:0.5rem;">
                    <div style="height:6px;width:{learner['progress']}%;background:{color};border-radius:8px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🤖 Generate AI Intervention Plan", use_container_width=True):
            with st.spinner("Analyzing at-risk learners..."):
                plan = get_ai_response(
                    "You are an educational data analyst. Provide specific intervention strategies.",
                    f"These learners are at risk of dropping out: {json.dumps(at_risk)}. Give 3 concrete interventions for each."
                )
            st.markdown(f'<div class="insight-card">{plan}</div>', unsafe_allow_html=True)

    with tab3:
        if st.button("🔍 Generate Curriculum Insights", use_container_width=True):
            with st.spinner("AI is analyzing curriculum effectiveness..."):
                insights = get_ai_response(
                    "You are an AI curriculum designer for an EdTech platform in Pakistan.",
                    "Based on 67% average completion rate, highest dropout at module 4 (Projects), and learners spending 3x more time on Python basics than other modules — give 5 specific curriculum improvement recommendations."
                )
            st.markdown(f'<div class="ai-chat-bubble">🤖 <strong>Curriculum Intelligence:</strong><br><br>{insights}</div>', unsafe_allow_html=True)


# ─── Router ────────────────────────────────────────────────────────────────────
render_sidebar()

page_map = {
    "dashboard": page_dashboard,
    "onboarding": page_onboarding,
    "courses": page_courses,
    "ai_tutor": page_ai_tutor,
    "quiz": page_quiz,
    "analytics": page_analytics,
    "learning_path": page_learning_path,
    "instructor": page_instructor,
}

current_page = page_map.get(st.session_state.page, page_dashboard)
current_page()
