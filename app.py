import streamlit as st
import requests
import json
import math

# ── Page config ──
st.set_page_config(
    page_title="AI Text Tools",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

API_KEY = st.secrets["RYNE_API_KEY"]

# ── Custom CSS for dark aesthetic ──
st.markdown("""
<style>
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Global */
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #0d1321 50%, #0a0e1a 100%);
    }

    /* Header */
    .app-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
    }
    .app-header h1 {
        background: linear-gradient(135deg, #a78bfa, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 0.25rem;
    }
    .app-header p {
        color: #64748b;
        font-size: 0.9rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }

    /* Section headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
        padding-top: 1rem;
    }
    .section-icon {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
    }
    .section-icon-detect {
        background: rgba(124, 58, 237, 0.15);
    }
    .section-icon-humanize {
        background: rgba(59, 130, 246, 0.15);
    }
    .section-title {
        color: #e2e8f0;
        font-size: 1.3rem;
        font-weight: 600;
        margin: 0;
    }
    .section-subtitle {
        color: #64748b;
        font-size: 0.8rem;
        margin: 0;
    }

    /* Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    .glass-card::before {
        content: "";
        position: absolute;
        inset: 0;
        border-radius: 12px;
        padding: 1px;
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.2), rgba(59, 130, 246, 0.05), transparent);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        pointer-events: none;
    }

    /* Score gauge */
    .gauge-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
    }
    .gauge-score {
        font-size: 2.5rem;
        font-weight: 800;
        line-height: 1;
    }
    .gauge-label {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .gauge-status {
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* Score comparison banner */
    .score-banner {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 2rem;
        padding: 1.25rem;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        margin: 1rem 0;
    }
    .score-item {
        text-align: center;
    }
    .score-item-label {
        font-size: 0.65rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-bottom: 0.25rem;
    }
    .score-item-value {
        font-size: 1.75rem;
        font-weight: 800;
    }
    .score-arrow {
        color: #7c3aed;
        font-size: 1.5rem;
    }

    /* Sentence highlighting */
    .sentence-ai {
        background: rgba(239, 68, 68, 0.15);
        border-bottom: 1.5px solid rgba(239, 68, 68, 0.3);
        padding: 1px 3px;
        border-radius: 3px;
    }
    .sentence-human {
        background: rgba(34, 197, 94, 0.08);
        padding: 1px 3px;
        border-radius: 3px;
    }

    /* Legend */
    .legend {
        display: flex;
        gap: 1.5rem;
        margin-bottom: 0.75rem;
    }
    .legend-item {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        font-size: 0.75rem;
        color: #64748b;
    }
    .legend-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
    }

    /* Badge */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.3rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-green {
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.25);
        color: #4ade80;
    }
    .badge-yellow {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.25);
        color: #fbbf24;
    }
    .badge-red {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.25);
        color: #f87171;
    }

    /* Divider */
    .styled-divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(124, 58, 237, 0.2), transparent);
        margin: 2.5rem 0;
    }

    /* Text display box */
    .text-display {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 10px;
        padding: 1rem;
        font-size: 0.9rem;
        line-height: 1.7;
        color: #cbd5e1;
        max-height: 250px;
        overflow-y: auto;
    }

    /* Streamlit overrides */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        font-size: 0.9rem !important;
    }
    .stTextArea textarea:focus {
        border-color: rgba(124, 58, 237, 0.4) !important;
        box-shadow: 0 0 0 1px rgba(124, 58, 237, 0.2) !important;
    }
    .stTextInput input {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }
    .stTextInput input:focus {
        border-color: rgba(124, 58, 237, 0.4) !important;
        box-shadow: 0 0 0 1px rgba(124, 58, 237, 0.2) !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed, #6d28d9) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.25) !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.35) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:disabled {
        opacity: 0.4 !important;
        box-shadow: none !important;
    }

    /* Streamlit label styling */
    .stTextArea label, .stTextInput label {
        color: #94a3b8 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
    }

    /* Columns gap */
    [data-testid="column"] {
        padding: 0 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


# ── Helper functions ──

def get_score_color(score: float) -> str:
    if score <= 25:
        return "#22c55e"
    elif score <= 50:
        return "#a3e635"
    elif score <= 75:
        return "#f59e0b"
    return "#ef4444"


def get_score_label(score: float) -> str:
    if score <= 25:
        return "Likely Human"
    elif score <= 50:
        return "Mixed"
    elif score <= 75:
        return "Likely AI"
    return "AI Generated"


def get_badge_class(risk: str) -> str:
    lower = risk.lower()
    if lower == "low":
        return "badge-green"
    elif lower == "medium":
        return "badge-yellow"
    return "badge-red"


def render_gauge(score: float, size: int = 160) -> str:
    color = get_score_color(score)
    label = get_score_label(score)
    stroke_width = size * 0.07
    radius = (size - stroke_width) / 2
    circumference = 2 * math.pi * radius
    clamped = max(0, min(score, 100))
    offset = circumference - (clamped / 100) * circumference

    return f"""
    <div class="gauge-container">
        <svg width="{size}" height="{size}" style="transform: rotate(-90deg); filter: drop-shadow(0 0 8px {color}40);">
            <circle cx="{size/2}" cy="{size/2}" r="{radius}" fill="none"
                    stroke="rgba(255,255,255,0.06)" stroke-width="{stroke_width}"/>
            <circle cx="{size/2}" cy="{size/2}" r="{radius}" fill="none"
                    stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round"
                    stroke-dasharray="{circumference}" stroke-dashoffset="{offset}"
                    style="transition: all 0.8s ease-in-out;"/>
        </svg>
        <div style="margin-top: -{size - 10}px; margin-bottom: {size/2 - 25}px; text-align: center;">
            <span class="gauge-score" style="color: {color};">{round(score)}%</span><br>
            <span class="gauge-label">AI Score</span>
        </div>
        <span class="gauge-status" style="color: {color};">{label}</span>
    </div>
    """


def render_mini_gauge(score: float) -> str:
    color = get_score_color(score)
    return f'<span style="font-size: 1.5rem; font-weight: 800; color: {color};">{round(score)}%</span>'


def detect_ai(text: str) -> dict | None:
    try:
        resp = requests.post(
            "https://ryne.ai/api/ai-score",
            json={"text": text, "user_id": API_KEY},
            timeout=30,
        )
        if resp.ok:
            return resp.json()
        else:
            st.error(f"Detection API error: {resp.status_code} — {resp.text}")
            return None
    except Exception as e:
        st.error(f"Detection failed: {e}")
        return None


def humanize_text(text: str, tone: str, purpose: str, language: str) -> str | None:
    try:
        resp = requests.post(
            "https://ryne.ai/api/humanizer/models/supernova",
            json={
                "text": text,
                "tone": tone or "professional",
                "purpose": purpose or "general",
                "language": language or "english",
                "user_id": API_KEY,
                "shouldStream": False,
            },
            timeout=60,
        )
        if resp.ok:
            data = resp.json()
            return data.get("content", "")
        else:
            st.error(f"Humanizer API error: {resp.status_code} — {resp.text}")
            return None
    except Exception as e:
        st.error(f"Humanization failed: {e}")
        return None


def render_sentences(sentences: list) -> str:
    html = """
    <div class="legend">
        <div class="legend-item"><div class="legend-dot" style="background: rgba(34, 197, 94, 0.5);"></div>Human</div>
        <div class="legend-item"><div class="legend-dot" style="background: rgba(239, 68, 68, 0.5);"></div>AI-detected</div>
    </div>
    <div style="line-height: 1.8; font-size: 0.9rem; color: #cbd5e1;">
    """
    for s in sentences:
        css_class = "sentence-ai" if s.get("isAI") else "sentence-human"
        prob = s.get("aiProbability", 0)
        title = f"AI: {prob:.1f}%"
        html += f'<span class="{css_class}" title="{title}">{s["text"]}</span> '
    html += "</div>"
    return html


# ── App header ──
st.markdown("""
<div class="app-header">
    <h1>AI Text Tools</h1>
    <p>Detection & Humanizer</p>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# SECTION 1: AI DETECTION
# ══════════════════════════════════════════════

st.markdown("""
<div class="section-header">
    <div class="section-icon section-icon-detect">🔍</div>
    <div>
        <p class="section-title">AI Detection</p>
        <p class="section-subtitle">Paste text to analyze for AI-generated content</p>
    </div>
</div>
""", unsafe_allow_html=True)

detect_text = st.text_area(
    "Text to analyze",
    height=180,
    placeholder="Paste or type text here to check for AI-generated content...",
    key="detect_input",
)

col_btn, col_info = st.columns([1, 3])
with col_btn:
    detect_clicked = st.button("🔍  Analyze Text", disabled=len(detect_text) < 50, use_container_width=True)
with col_info:
    if 0 < len(detect_text) < 50:
        st.caption(f"⚠️ Need {50 - len(detect_text)} more characters")
    elif len(detect_text) >= 50:
        st.caption(f"✓ {len(detect_text)} characters — ready to analyze")

if detect_clicked and len(detect_text) >= 50:
    with st.spinner("Analyzing text..."):
        result = detect_ai(detect_text)
    if result:
        st.session_state["detect_result"] = result

if "detect_result" in st.session_state:
    result = st.session_state["detect_result"]
    ai_score = result.get("aiScore", 0)
    classification = result.get("classification", "UNKNOWN")
    details = result.get("details", {})
    analysis = details.get("analysis", {})
    risk = analysis.get("risk", "Unknown")
    suggestion = analysis.get("suggestion", "")
    sentences = details.get("sentences", [])

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    col_gauge, col_sentences = st.columns([1, 2])

    with col_gauge:
        st.markdown(render_gauge(ai_score), unsafe_allow_html=True)
        badge_class = get_badge_class(risk)
        st.markdown(
            f'<div style="text-align:center; margin-top: 0.5rem;">'
            f'<span class="badge {badge_class}">{classification.replace("_", " ")}</span>'
            f'<div style="font-size: 0.7rem; color: #64748b; margin-top: 0.5rem;">{risk} Risk</div>'
            f'<div style="font-size: 0.8rem; color: #64748b; margin-top: 0.5rem; max-width: 220px; margin-left: auto; margin-right: auto;">{suggestion}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with col_sentences:
        st.markdown(
            '<div style="font-size: 0.8rem; font-weight: 500; color: #64748b; margin-bottom: 0.5rem;">SENTENCE ANALYSIS</div>',
            unsafe_allow_html=True,
        )
        if sentences:
            st.markdown(
                f'<div class="text-display">{render_sentences(sentences)}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.caption("No sentence-level data available.")

    st.markdown("</div>", unsafe_allow_html=True)


# ── Divider ──
st.markdown('<hr class="styled-divider">', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# SECTION 2: AI HUMANIZER
# ══════════════════════════════════════════════

st.markdown("""
<div class="section-header">
    <div class="section-icon section-icon-humanize">✨</div>
    <div>
        <p class="section-title">AI Humanizer</p>
        <p class="section-subtitle">Transform AI text into natural, undetectable writing</p>
    </div>
</div>
""", unsafe_allow_html=True)

humanize_text_input = st.text_area(
    "Text to humanize",
    height=180,
    placeholder="Paste AI-generated text here to humanize it...",
    key="humanize_input",
)

st.markdown(
    '<div style="font-size: 0.7rem; font-weight: 500; color: #64748b; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem; margin-top: 1rem;">Settings</div>',
    unsafe_allow_html=True,
)
col_tone, col_purpose, col_lang = st.columns(3)
with col_tone:
    tone = st.text_input("Tone", value="professional", placeholder="Professional, Casual...")
with col_purpose:
    purpose = st.text_input("Purpose", value="essay", placeholder="Essay, Blog post...")
with col_lang:
    language = st.text_input("Language", value="english", placeholder="English, Spanish...")

humanize_clicked = st.button(
    "✨  Humanize Text",
    disabled=len(humanize_text_input) < 50,
    use_container_width=False,
)

if 0 < len(humanize_text_input) < 50:
    st.caption(f"⚠️ Need {50 - len(humanize_text_input)} more characters")

if humanize_clicked and len(humanize_text_input) >= 50:
    # Step 1: Detect original
    with st.spinner("Detecting original text..."):
        input_detection = detect_ai(humanize_text_input)

    # Step 2: Humanize
    with st.spinner("Humanizing text..."):
        humanized = humanize_text(humanize_text_input, tone, purpose, language)

    if humanized:
        # Step 3: Detect humanized output
        with st.spinner("Checking humanized text..."):
            output_detection = detect_ai(humanized)

        st.session_state["humanizer_result"] = {
            "input_text": humanize_text_input,
            "output_text": humanized,
            "input_detection": input_detection,
            "output_detection": output_detection,
        }

if "humanizer_result" in st.session_state:
    hr = st.session_state["humanizer_result"]
    input_det = hr.get("input_detection")
    output_det = hr.get("output_detection")

    # Score comparison banner
    if input_det and output_det:
        before_score = input_det.get("aiScore", 0)
        after_score = output_det.get("aiScore", 0)
        before_color = get_score_color(before_score)
        after_color = get_score_color(after_score)
        st.markdown(
            f"""
            <div class="score-banner">
                <div class="score-item">
                    <div class="score-item-label">Before</div>
                    <div class="score-item-value" style="color: {before_color};">{round(before_score)}%</div>
                </div>
                <div class="score-arrow">→</div>
                <div class="score-item">
                    <div class="score-item-label">After</div>
                    <div class="score-item-value" style="color: {after_color};">{round(after_score)}%</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Side-by-side cards
    col_original, col_humanized = st.columns(2)

    with col_original:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        orig_label = "ORIGINAL"
        if input_det:
            s = input_det.get("aiScore", 0)
            c = get_score_color(s)
            st.markdown(
                f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">'
                f'<span style="font-size: 0.75rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.1em;">{orig_label}</span>'
                f'<span style="font-size: 1.25rem; font-weight: 800; color: {c};">{round(s)}%</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<span style="font-size: 0.75rem; font-weight: 600; color: #64748b;">{orig_label}</span>',
                unsafe_allow_html=True,
            )
        st.markdown(
            f'<div class="text-display">{hr["input_text"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_humanized:
        st.markdown(
            '<div class="glass-card" style="border-color: rgba(124, 58, 237, 0.15); box-shadow: 0 0 20px rgba(124, 58, 237, 0.08);">',
            unsafe_allow_html=True,
        )
        hum_label = "HUMANIZED"
        if output_det:
            s = output_det.get("aiScore", 0)
            c = get_score_color(s)
            st.markdown(
                f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">'
                f'<span style="font-size: 0.75rem; font-weight: 600; color: #7c3aed; text-transform: uppercase; letter-spacing: 0.1em;">{hum_label}</span>'
                f'<span style="font-size: 1.25rem; font-weight: 800; color: {c};">{round(s)}%</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<span style="font-size: 0.75rem; font-weight: 600; color: #7c3aed;">{hum_label}</span>',
                unsafe_allow_html=True,
            )
        st.markdown(
            f'<div class="text-display">{hr["output_text"]}</div>',
            unsafe_allow_html=True,
        )
        # Copy button
        st.code(hr["output_text"], language=None)
        st.markdown("</div>", unsafe_allow_html=True)
