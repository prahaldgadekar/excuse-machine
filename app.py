import streamlit as st
import random
import os
from dotenv import load_dotenv
from groq import Groq

# ── Load API key ───────────────────────────────────────────────────────────────
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).parent / ".env")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    try:
        GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        pass

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EXCUSE.EXE",
    page_icon="💻",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
# CSS + ANIMATIONS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Base ─────────────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1rem 1rem 4rem 1rem !important; max-width: 100% !important; }

/* ── Boot screen overlay ─────────────────────────────────────────────────── */
#boot-screen {
    position: fixed; inset: 0; z-index: 9999;
    background: #0a0a0f;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    animation: boot-fade 0.5s ease 2.8s forwards;
    pointer-events: none;
}
@keyframes boot-fade { to { opacity: 0; visibility: hidden; } }
#boot-text {
    font-family: 'Share Tech Mono', monospace;
    color: #00ff88; font-size: clamp(0.68rem, 3vw, 0.92rem);
    text-align: left; width: clamp(260px, 80vw, 480px);
    line-height: 2.2;
}
#boot-bar-wrap {
    width: clamp(260px, 80vw, 480px);
    background: #1a1a2e; height: 4px; border-radius: 2px;
    margin-top: 18px; overflow: hidden;
}
#boot-bar {
    height: 100%; width: 0; background: #00ff88; border-radius: 2px;
    animation: bar-fill 2.4s ease 0.2s forwards;
    box-shadow: 0 0 12px #00ff88;
}
@keyframes bar-fill { to { width: 100%; } }
.boot-line { opacity: 0; animation: line-appear 0.1s ease forwards; }
.boot-line:nth-child(1) { animation-delay: 0.1s; }
.boot-line:nth-child(2) { animation-delay: 0.45s; }
.boot-line:nth-child(3) { animation-delay: 0.8s; }
.boot-line:nth-child(4) { animation-delay: 1.1s; }
.boot-line:nth-child(5) { animation-delay: 1.4s; }
.boot-line:nth-child(6) { animation-delay: 1.75s; }
.boot-line:nth-child(7) { animation-delay: 2.1s; }
@keyframes line-appear { to { opacity: 1; } }

/* ── Matrix rain canvas ──────────────────────────────────────────────────── */
#matrix-canvas {
    position: fixed; top: 0; left: 0;
    width: 100vw; height: 100vh;
    z-index: -1; opacity: 0.07;
    pointer-events: none;
}

/* ── Cursor trail ────────────────────────────────────────────────────────── */
.cursor-dot {
    position: fixed; border-radius: 50%;
    pointer-events: none; z-index: 9998;
    transform: translate(-50%, -50%);
    background: #00ff88;
    box-shadow: 0 0 6px #00ff88;
    transition: opacity 0.3s;
}

/* ── Hero header wrapper ──────────────────────────────────────────────────── */
.hero-wrap {
    position: relative;
    text-align: center;
    padding: 2.8rem 1rem 2rem;
    margin-bottom: 0.5rem;
    overflow: hidden;
}
/* animated horizontal scan bar behind title */
.hero-wrap::before {
    content: '';
    position: absolute; left: -10%; right: -10%;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00ff88, #00ffff, #00ff88, transparent);
    animation: hero-scan 3s ease-in-out infinite;
    opacity: 0.5;
}
@keyframes hero-scan {
    0%   { top: 0%;   opacity: 0; }
    10%  { opacity: 0.6; }
    90%  { opacity: 0.4; }
    100% { top: 100%; opacity: 0; }
}
/* corner brackets decoration */
.hero-corner {
    position: absolute;
    width: 28px; height: 28px;
    border-color: rgba(0,255,136,0.45);
    border-style: solid;
    animation: corner-pulse 3s ease-in-out infinite;
}
.hero-corner.tl { top: 14px; left: 14px; border-width: 2px 0 0 2px; }
.hero-corner.tr { top: 14px; right: 14px; border-width: 2px 2px 0 0; }
.hero-corner.bl { bottom: 14px; left: 14px; border-width: 0 0 2px 2px; }
.hero-corner.br { bottom: 14px; right: 14px; border-width: 0 2px 2px 0; }
@keyframes corner-pulse {
    0%,100% { border-color: rgba(0,255,136,0.3); }
    50%      { border-color: rgba(0,255,136,0.9); box-shadow: 0 0 12px rgba(0,255,136,0.4); }
}

/* ── Glitch title ─────────────────────────────────────────────────────────── */
.big-title {
    font-family: 'Share Tech Mono', monospace;
    font-size: clamp(2.8rem, 12vw, 6rem);
    font-weight: 900;
    color: #00ff88;
    text-align: center;
    letter-spacing: clamp(4px, 3vw, 16px);
    position: relative;
    display: inline-block;
    animation: glitch-anim 3s infinite, neon-flicker 8s ease-in-out infinite, title-float 6s ease-in-out infinite;
    text-shadow:
        0 0 10px rgba(0,255,136,1),
        0 0 30px rgba(0,255,136,0.7),
        0 0 80px rgba(0,255,136,0.3),
        0 0 160px rgba(0,255,136,0.1);
}
.big-title::before, .big-title::after {
    content: attr(data-text);
    position: absolute; left: 0; right: 0;
    text-align: center;
}
.big-title::before {
    color: #ff00ff;
    animation: glitch-before 3s infinite;
    clip-path: polygon(0 30%, 100% 30%, 100% 50%, 0 50%);
    opacity: 0.75;
    text-shadow: 0 0 20px #ff00ff;
}
.big-title::after {
    color: #00ffff;
    animation: glitch-after 3s infinite;
    clip-path: polygon(0 60%, 100% 60%, 100% 78%, 0 78%);
    opacity: 0.75;
    text-shadow: 0 0 20px #00ffff;
}
/* NEW: subtle float */
@keyframes title-float {
    0%,100% { transform: translateY(0px); }
    50%      { transform: translateY(-6px); }
}
@keyframes glitch-anim {
    0%,88%,100% { transform: translateY(0px); }
    89%  { transform: skewX(-4deg) translateX(3px) translateY(0); }
    90%  { transform: skewX(4deg)  translateX(-3px) translateY(0); }
    91%  { transform: none; }
    92%  { transform: skewX(-2deg) translateX(5px) translateY(0); }
    93%  { transform: none; }
}
/* NEW: neon flicker */
@keyframes neon-flicker {
    0%,19%,21%,23%,25%,54%,56%,100% {
        text-shadow: 0 0 10px rgba(0,255,136,1), 0 0 30px rgba(0,255,136,0.7), 0 0 80px rgba(0,255,136,0.3);
        opacity: 1;
    }
    20%,24%,55% {
        text-shadow: none;
        opacity: 0.4;
    }
}
@keyframes glitch-before {
    0%,88%,100% { transform: none; opacity: 0; }
    89% { transform: translateX(-6px) skewX(-2deg); opacity: 0.8; }
    90% { transform: translateX(6px);  opacity: 0.8; }
    91% { opacity: 0; }
    92% { transform: translateX(-3px); opacity: 0.6; }
    93% { opacity: 0; }
}
@keyframes glitch-after {
    0%,88%,100% { transform: none; opacity: 0; }
    89% { transform: translateX(6px) skewX(2deg);  opacity: 0.8; }
    90% { transform: translateX(-6px); opacity: 0.8; }
    91% { opacity: 0; }
    92% { transform: translateX(3px);  opacity: 0.6; }
    93% { opacity: 0; }
}

/* ── Version badge beside title ───────────────────────────────────────────── */
.hero-version {
    font-family: 'Share Tech Mono', monospace;
    font-size: clamp(0.55rem, 2vw, 0.7rem);
    color: #00ff88;
    border: 1px solid rgba(0,255,136,0.4);
    background: rgba(0,255,136,0.07);
    padding: 2px 10px;
    border-radius: 4px;
    letter-spacing: 2px;
    display: inline-block;
    margin-bottom: 10px;
    animation: fadeup 1s ease 0.3s both;
}
/* ── Tag row under title ──────────────────────────────────────────────────── */
.hero-tags {
    display: flex; gap: 8px; justify-content: center; flex-wrap: wrap;
    margin-top: 14px;
    animation: fadeup 1s ease 1s both;
}
.hero-tag {
    font-family: 'Share Tech Mono', monospace;
    font-size: clamp(0.55rem, 2vw, 0.65rem);
    padding: 3px 12px; border-radius: 100px;
    border: 1px solid rgba(0,255,136,0.25);
    color: rgba(0,255,136,0.7);
    background: rgba(0,255,136,0.05);
    letter-spacing: 1px;
    white-space: nowrap;
    animation: hero-tag-in 0.5s cubic-bezier(0.34,1.56,0.64,1) both;
}
.hero-tag:nth-child(1){animation-delay:1.0s}.hero-tag:nth-child(2){animation-delay:1.15s}
.hero-tag:nth-child(3){animation-delay:1.3s}.hero-tag:nth-child(4){animation-delay:1.45s}
@keyframes hero-tag-in {
    from { opacity:0; transform: scale(0.6) translateY(8px); }
    to   { opacity:1; transform: scale(1) translateY(0); }
}
@keyframes fadeup {
    from { opacity:0; transform:translateY(12px); }
    to   { opacity:1; transform:translateY(0); }
}

/* ── Subtitle typewriter ──────────────────────────────────────────────────── */
.subtitle {
    font-family: 'Share Tech Mono', monospace;
    text-align: center;
    color: #5a5a9a;
    font-size: clamp(0.75rem, 3vw, 1rem);
    margin-top: 10px;
    overflow: hidden;
    white-space: nowrap;
    border-right: 2px solid #00ff88;
    width: fit-content;
    margin-left: auto; margin-right: auto;
    animation: typewriter 2.5s steps(45,end) 0.5s both, blink-caret 0.75s step-end infinite;
}
@keyframes typewriter   { from { width: 0; } to { width: 100%; } }
@keyframes blink-caret  { 0%,100%{border-color:#00ff88} 50%{border-color:transparent} }

/* ── Glowing underline below hero ─────────────────────────────────────────── */
.hero-line {
    height: 1px;
    background: linear-gradient(90deg, transparent, #00ff88, #00ffff, #00ff88, transparent);
    margin: 1.4rem 0 0;
    animation: hero-line-in 1.5s ease 1.5s both;
    box-shadow: 0 0 12px rgba(0,255,136,0.4);
}
@keyframes hero-line-in {
    from { transform: scaleX(0); opacity:0; }
    to   { transform: scaleX(1); opacity:1; }
}

/* ── Floating particles ───────────────────────────────────────────────────── */
.particles { position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden; }
.particle {
    position: absolute; width: 3px; height: 3px;
    background: #00ff88; border-radius: 50%;
    animation: float-up linear infinite;
    opacity: 0;
}
@keyframes float-up {
    0%   { transform: translateY(100vh) scale(0); opacity: 0; }
    10%  { opacity: 0.6; }
    90%  { opacity: 0.3; }
    100% { transform: translateY(-10vh) scale(1.5); opacity: 0; }
}

/* ── Excuse card ──────────────────────────────────────────────────────────── */
.excuse-box {
    background: linear-gradient(135deg, #10101a 0%, #0d0d1a 100%);
    border: 1px solid #00ff88;
    border-radius: 14px;
    padding: clamp(14px,4vw,26px) clamp(14px,4vw,30px);
    font-family: 'Share Tech Mono', monospace;
    font-size: clamp(0.92rem, 3.5vw, 1.1rem);
    line-height: 1.8;
    color: #e0e0f0;
    margin: 14px 0;
    word-break: break-word;
    position: relative;
    overflow: hidden;
    animation: card-enter 0.5s cubic-bezier(0.22,1,0.36,1), border-breathe 4s ease-in-out 0.5s infinite;
}
/* NEW: card border breathe */
@keyframes border-breathe {
    0%,100% { box-shadow: 0 0 0 1px rgba(0,255,136,0.15), 0 0 20px rgba(0,255,136,0.06); }
    50%      { box-shadow: 0 0 0 1px rgba(0,255,136,0.5),  0 0 40px rgba(0,255,136,0.18); }
}
.excuse-box::before {
    content: '';
    position: absolute; inset: 0;
    border-radius: 14px;
    background: linear-gradient(90deg, transparent 0%, rgba(0,255,136,0.04) 50%, transparent 100%);
    background-size: 200% 100%;
    animation: shimmer 3s linear infinite;
}
@keyframes card-enter {
    from { opacity: 0; transform: translateY(20px) scale(0.97); }
    to   { opacity: 1; transform: none; }
}
@keyframes shimmer {
    from { background-position: -200% 0; }
    to   { background-position:  200% 0; }
}
.excuse-box::after {
    content: '';
    position: absolute; left: 0; right: 0;
    height: 40px;
    background: linear-gradient(transparent, rgba(0,255,136,0.04), transparent);
    animation: scanline 4s linear infinite;
    pointer-events: none;
}
@keyframes scanline {
    from { top: -40px; }
    to   { top: 110%; }
}

/* ── Category tags ────────────────────────────────────────────────────────── */
.tag {
    display: inline-block; padding: 3px 12px; border-radius: 20px;
    font-size: clamp(0.6rem, 2.5vw, 0.72rem);
    font-family: 'Share Tech Mono', monospace;
    letter-spacing: 1px; font-weight: bold; margin-bottom: 8px;
    white-space: nowrap;
}
.tag-DEVELOPER   { background:rgba(0,200,255,0.12); color:#60d8ff; border:1px solid #007aaa;
                   animation: tag-pop 0.4s cubic-bezier(0.34,1.56,0.64,1), tag-glow-blue   3s ease-in-out infinite; }
.tag-COSMIC      { background:rgba(138,43,226,0.2);  color:#bf7fff; border:1px solid #7a00cc;
                   animation: tag-pop 0.4s cubic-bezier(0.34,1.56,0.64,1), tag-glow-purple 3s ease-in-out infinite; }
.tag-PHYSICAL    { background:rgba(255,100,0,0.15);  color:#ff8040; border:1px solid #cc5200;
                   animation: tag-pop 0.4s cubic-bezier(0.34,1.56,0.64,1), tag-glow-orange 3s ease-in-out infinite; }
.tag-BLAMING     { background:rgba(255,60,90,0.15);  color:#ff7090; border:1px solid #aa0020;
                   animation: tag-pop 0.4s cubic-bezier(0.34,1.56,0.64,1), tag-glow-red    3s ease-in-out infinite; }
.tag-EXISTENTIAL { background:rgba(255,230,0,0.10);  color:#ffe660; border:1px solid #998800;
                   animation: tag-pop 0.4s cubic-bezier(0.34,1.56,0.64,1), tag-glow-yellow 3s ease-in-out infinite; }
@keyframes tag-pop    { from { transform: scale(0); opacity: 0; } to { transform: scale(1); opacity: 1; } }
/* NEW: tag colour-specific glows */
@keyframes tag-glow-blue   { 0%,100%{box-shadow:0 0 6px rgba(0,200,255,0.2)}  50%{box-shadow:0 0 18px rgba(0,200,255,0.7)} }
@keyframes tag-glow-purple { 0%,100%{box-shadow:0 0 6px rgba(138,43,226,0.3)} 50%{box-shadow:0 0 18px rgba(138,43,226,0.8)} }
@keyframes tag-glow-orange { 0%,100%{box-shadow:0 0 6px rgba(255,100,0,0.2)}  50%{box-shadow:0 0 18px rgba(255,100,0,0.7)} }
@keyframes tag-glow-red    { 0%,100%{box-shadow:0 0 6px rgba(255,60,90,0.2)}  50%{box-shadow:0 0 18px rgba(255,60,90,0.7)} }
@keyframes tag-glow-yellow { 0%,100%{box-shadow:0 0 6px rgba(255,230,0,0.2)}  50%{box-shadow:0 0 18px rgba(255,230,0,0.7)} }

/* ── AI badge ─────────────────────────────────────────────────────────────── */
.ai-badge {
    background: rgba(0,255,136,0.1); color: #00ff88;
    border: 1px solid #00ff88; border-radius: 20px;
    padding: 2px 10px;
    font-size: clamp(0.58rem, 2vw, 0.7rem);
    font-family: 'Share Tech Mono', monospace; letter-spacing: 1px;
    white-space: nowrap;
    animation: pulse-badge 2s ease-in-out infinite;
}
@keyframes pulse-badge {
    0%,100% { box-shadow: 0 0 4px rgba(0,255,136,0.4); }
    50%      { box-shadow: 0 0 14px rgba(0,255,136,0.9); }
}

/* ── Leaderboard item ─────────────────────────────────────────────────────── */
.lb-item {
    background: linear-gradient(135deg, #10101a, #0d0d18);
    border: 1px solid #1e1e2e;
    border-radius: 10px;
    padding: clamp(10px,3vw,14px) clamp(10px,3vw,18px);
    margin: 6px 0; font-family: 'Share Tech Mono', monospace;
    word-break: break-word;
    transition: border-color 0.3s, box-shadow 0.3s, transform 0.2s;
    animation: slide-in 0.4s ease backwards;
}
.lb-item:hover {
    border-color: #00ff88;
    box-shadow: 0 0 16px rgba(0,255,136,0.15);
    transform: translateX(4px);
}
@keyframes slide-in {
    from { opacity: 0; transform: translateX(-20px); }
    to   { opacity: 1; transform: none; }
}

/* ── Metrics ──────────────────────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: #10101a; border: 1px solid #1e1e2e; border-radius: 10px;
    padding: 8px !important; text-align: center;
    transition: border-color 0.3s, box-shadow 0.3s;
    animation: metric-pop 0.6s cubic-bezier(0.34,1.56,0.64,1) backwards;
}
[data-testid="stMetric"]:hover {
    border-color: #00ff88;
    box-shadow: 0 0 20px rgba(0,255,136,0.15);
}
[data-testid="stMetric"]:nth-child(1) { animation-delay: 0.1s; }
[data-testid="stMetric"]:nth-child(2) { animation-delay: 0.2s; }
[data-testid="stMetric"]:nth-child(3) { animation-delay: 0.3s; }
[data-testid="stMetric"]:nth-child(4) { animation-delay: 0.4s; }
@keyframes metric-pop {
    from { opacity: 0; transform: scale(0.8); }
    to   { opacity: 1; transform: scale(1); }
}
[data-testid="stMetricLabel"] p  { font-size: clamp(0.55rem,2vw,0.78rem) !important; font-family: 'Share Tech Mono', monospace !important; }
[data-testid="stMetricValue"]    { font-size: clamp(1rem,4vw,1.5rem) !important; font-family: 'Share Tech Mono', monospace !important; color: #00ff88 !important; }

/* ── Buttons ──────────────────────────────────────────────────────────────── */
.stButton > button {
    font-family: 'Share Tech Mono', monospace !important;
    font-weight: bold !important; letter-spacing: 2px !important;
    min-height: 48px !important;
    font-size: clamp(0.82rem, 3vw, 1rem) !important;
    border-radius: 10px !important;
    touch-action: manipulation;
    transition: transform 0.15s, box-shadow 0.15s, background 0.15s !important;
    position: relative; overflow: hidden;
}
.stButton > button:hover {
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: 0 8px 25px rgba(0,255,136,0.3) !important;
}
.stButton > button:active {
    transform: scale(0.97) !important;
    animation: btn-shake 0.3s ease !important;
}
.stButton > button::after {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(circle at center, rgba(255,255,255,0.2) 0%, transparent 70%);
    opacity: 0; transition: opacity 0.3s;
    border-radius: 10px;
}
.stButton > button:active::after { opacity: 1; }
@keyframes btn-shake {
    0%,100% { transform: translateX(0); }
    25%      { transform: translateX(-4px); }
    75%      { transform: translateX(4px);  }
}
/* NEW: primary button idle glow pulse */
.stButton > button[kind="primary"] {
    animation: btn-glow-idle 3s ease-in-out infinite;
}
@keyframes btn-glow-idle {
    0%,100% { box-shadow: 0 0 8px rgba(0,255,136,0.2); }
    50%      { box-shadow: 0 0 28px rgba(0,255,136,0.55), 0 0 52px rgba(0,255,136,0.15); }
}

/* ── Tabs ─────────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    overflow-x: auto; flex-wrap: nowrap;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none; gap: 4px; padding-bottom: 2px;
}
.stTabs [data-baseweb="tab-list"]::-webkit-scrollbar { display: none; }
.stTabs [data-baseweb="tab"] {
    white-space: nowrap;
    font-size: clamp(0.72rem, 3vw, 0.9rem) !important;
    padding: 8px 12px !important; min-height: 44px;
    font-family: 'Share Tech Mono', monospace !important;
    transition: color 0.2s, border-color 0.2s !important;
}
/* NEW: active tab text glow */
.stTabs [aria-selected="true"] {
    animation: tab-glow 2s ease-in-out infinite !important;
}
@keyframes tab-glow {
    0%,100% { text-shadow: 0 0 6px rgba(0,255,136,0.4); }
    50%      { text-shadow: 0 0 18px rgba(0,255,136,0.95), 0 0 32px rgba(0,255,136,0.3); }
}

/* ── Selectbox & textarea ─────────────────────────────────────────────────── */
.stSelectbox > div > div { min-height: 44px; font-family: 'Share Tech Mono', monospace; }
.stTextArea textarea    { font-family: 'Share Tech Mono', monospace; font-size: clamp(0.85rem,3vw,0.95rem) !important; }
/* NEW: input focus glow */
.stTextArea textarea:focus {
    border-color: #00ff88 !important;
    box-shadow: 0 0 0 2px rgba(0,255,136,0.25), 0 0 20px rgba(0,255,136,0.1) !important;
    transition: box-shadow 0.3s, border-color 0.3s !important;
}
.stTextInput input:focus {
    border-color: #00ff88 !important;
    box-shadow: 0 0 0 2px rgba(0,255,136,0.25), 0 0 20px rgba(0,255,136,0.1) !important;
    transition: box-shadow 0.3s !important;
}

/* ── Spinner animation ────────────────────────────────────────────────────── */
.stSpinner > div { border-color: #00ff88 transparent transparent transparent !important; }

/* ── Success/Error flash ──────────────────────────────────────────────────── */
.stSuccess, .stError { animation: flash-in 0.4s ease; }
@keyframes flash-in {
    from { opacity: 0; transform: translateY(-8px); }
    to   { opacity: 1; transform: none; }
}
/* NEW: success glow pulse */
.stSuccess {
    animation: flash-in 0.4s ease, success-pulse 2s ease-in-out 0.5s infinite !important;
}
@keyframes success-pulse {
    0%,100% { box-shadow: none; }
    50%      { box-shadow: 0 0 22px rgba(0,255,136,0.25); }
}

/* ── Divider glow ─────────────────────────────────────────────────────────── */
hr {
    border-color: rgba(0,255,136,0.2) !important;
    box-shadow: 0 0 8px rgba(0,255,136,0.1);
    animation: divider-expand 1s ease;
}
@keyframes divider-expand {
    from { transform: scaleX(0); opacity: 0; }
    to   { transform: scaleX(1); opacity: 1; }
}

/* ── Responsive ───────────────────────────────────────────────────────────── */
@media (max-width: 380px) {
    .stButton > button { padding: 10px 4px !important; font-size: 0.72rem !important; }
    div[data-testid="column"] { min-width: 0 !important; }
}
</style>

<!-- Boot screen -->
<div id="boot-screen">
  <div id="boot-text">
    <div class="boot-line">&gt; EXCUSE.EXE v2.0 initializing...</div>
    <div class="boot-line">&gt; Loading excuse database........... <span style="color:#ffe660">OK</span></div>
    <div class="boot-line">&gt; Connecting to Groq AI............. <span style="color:#ffe660">OK</span></div>
    <div class="boot-line">&gt; Warming up blame engine........... <span style="color:#ffe660">OK</span></div>
    <div class="boot-line">&gt; Disabling accountability module... <span style="color:#ff7090">DONE</span></div>
    <div class="boot-line">&gt; Zero regrets policy enforced...... <span style="color:#00ff88">ACTIVE</span></div>
    <div class="boot-line">&gt; <span style="color:#00ff88">System ready. Excuses online. 💻</span></div>
  </div>
  <div id="boot-bar-wrap"><div id="boot-bar"></div></div>
</div>

<!-- Matrix Rain Canvas -->
<canvas id="matrix-canvas"></canvas>

<!-- Floating Particles -->
<div class="particles" id="particles"></div>

<script>
// ── Matrix Rain ───────────────────────────────────────────────────────────────
(function(){
    const c = document.getElementById('matrix-canvas');
    if (!c) return;
    const ctx = c.getContext('2d');
    c.width  = window.innerWidth;
    c.height = window.innerHeight;
    const cols = Math.floor(c.width / 20);
    const drops = Array(cols).fill(1);
    const chars = '01アイウエオカキクケコABCDEFGHIJKLMNOPQRSTUVWXYZ{}[]<>/\\|';
    function draw(){
        ctx.fillStyle = 'rgba(10,10,15,0.05)';
        ctx.fillRect(0,0,c.width,c.height);
        ctx.fillStyle = '#00ff88';
        ctx.font = '14px monospace';
        drops.forEach((y,i)=>{
            const ch = chars[Math.floor(Math.random()*chars.length)];
            ctx.fillText(ch, i*20, y*20);
            if(y*20 > c.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        });
    }
    setInterval(draw, 60);
    window.addEventListener('resize',()=>{ c.width=window.innerWidth; c.height=window.innerHeight; });
})();

// ── Floating Particles ────────────────────────────────────────────────────────
(function(){
    const container = document.getElementById('particles');
    if (!container) return;
    const colors = ['#00ff88','#60d8ff','#bf7fff','#ff7090','#ffe660'];
    for(let i=0;i<30;i++){
        const p = document.createElement('div');
        p.className = 'particle';
        p.style.cssText = `
            left: ${Math.random()*100}vw;
            width:  ${Math.random()*4+1}px;
            height: ${Math.random()*4+1}px;
            background: ${colors[Math.floor(Math.random()*colors.length)]};
            animation-duration:  ${Math.random()*12+8}s;
            animation-delay:    -${Math.random()*15}s;
        `;
        container.appendChild(p);
    }
})();

// ── Cursor Trail ──────────────────────────────────────────────────────────────
(function(){
    const TRAIL = 10;
    const dots = [];
    for(let i=0;i<TRAIL;i++){
        const d = document.createElement('div');
        d.className = 'cursor-dot';
        const sz = Math.max(2, 7 - i*0.5);
        d.style.cssText = `width:${sz}px;height:${sz}px;opacity:${(1-i/TRAIL)*0.75};`;
        document.body.appendChild(d);
        dots.push(d);
    }
    let positions = Array(TRAIL).fill({x:-200,y:-200});
    let mx = -200, my = -200;
    document.addEventListener('mousemove', e => { mx=e.clientX; my=e.clientY; });
    (function loop(){
        positions = [{x:mx,y:my}, ...positions.slice(0,TRAIL-1)];
        dots.forEach((d,i) => {
            d.style.left = positions[i].x + 'px';
            d.style.top  = positions[i].y + 'px';
        });
        requestAnimationFrame(loop);
    })();
})();

// ── Typing effect on new excuse cards ────────────────────────────────────────
(function(){
    function applyTyping(){
        document.querySelectorAll('.excuse-box').forEach(box => {
            if(box.dataset.typed) return;
            box.dataset.typed = '1';
            const textNodes = [];
            box.childNodes.forEach(n => {
                if(n.nodeType === 3 && n.textContent.trim().length > 10) textNodes.push(n);
            });
            if(!textNodes.length) return;
            const node = textNodes[textNodes.length-1];
            const full = node.textContent;
            node.textContent = '';
            let i = 0;
            const iv = setInterval(()=>{
                node.textContent += full[i++];
                if(i >= full.length) clearInterval(iv);
            }, 16);
        });
    }
    new MutationObserver(applyTyping).observe(document.body, {childList:true, subtree:true});
    setTimeout(applyTyping, 600);
})();

// ── Metric count-up ───────────────────────────────────────────────────────────
(function(){
    function animateMetrics(){
        document.querySelectorAll('[data-testid="stMetricValue"]').forEach(el => {
            if(el.dataset.counted) return;
            const target = parseInt(el.textContent.replace(/\D/g,''));
            if(isNaN(target) || target === 0) return;
            el.dataset.counted = '1';
            const suffix = el.textContent.replace(/[\d]/g,'');
            let cur = 0;
            const step = Math.max(1, Math.floor(target/30));
            const iv = setInterval(()=>{
                cur = Math.min(cur+step, target);
                el.textContent = cur + suffix;
                if(cur >= target) clearInterval(iv);
            }, 35);
        });
    }
    new MutationObserver(animateMetrics).observe(document.body, {childList:true, subtree:true});
    setTimeout(animateMetrics, 900);
})();
</script>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════════
CATEGORIES = ["DEVELOPER", "COSMIC", "PHYSICAL", "BLAMING OTHERS", "EXISTENTIAL"]
ICONS = {"DEVELOPER":"👨‍💻","COSMIC":"🌌","PHYSICAL":"🖱️","BLAMING OTHERS":"😈","EXISTENTIAL":"🌀"}
TAG_CLASS = {
    "DEVELOPER":"tag-DEVELOPER","COSMIC":"tag-COSMIC","PHYSICAL":"tag-PHYSICAL",
    "BLAMING OTHERS":"tag-BLAMING","EXISTENTIAL":"tag-EXISTENTIAL",
}
DEFAULT_EXCUSES = [
    {"text": "It worked on my machine. Clearly the problem is the universe, not me.", "category": "DEVELOPER", "likes": 42},
    {"text": "npm install. That's it. That's the entire bug.", "category": "DEVELOPER", "likes": 88},
    {"text": "Mercury is in retrograde and apparently that affects JavaScript garbage collection now.", "category": "COSMIC", "likes": 31},
    {"text": "The intern touched it. I'm not allowed to say more for legal reasons.", "category": "BLAMING OTHERS", "likes": 75},
    {"text": "I was using tabs. The senior dev uses spaces. The merge conflict became sentient.", "category": "DEVELOPER", "likes": 60},
    {"text": "The cosmic radiation from a dying star in Andromeda flipped a bit in my RAM.", "category": "COSMIC", "likes": 29},
    {"text": "My rubber duck debugger quit. HR says it's a lifestyle choice.", "category": "PHYSICAL", "likes": 90},
    {"text": "The client said 'make it pop'. My server is now in the ICU.", "category": "BLAMING OTHERS", "likes": 77},
    {"text": "I upgraded Node.js. Everything broke. I downgraded. Still broken. Time is now a circle.", "category": "DEVELOPER", "likes": 95},
    {"text": "Git blamed me. I blamed Git. We've reached an impasse.", "category": "DEVELOPER", "likes": 83},
    {"text": "The code is fine. It's the concept of 'working software' that's broken.", "category": "EXISTENTIAL", "likes": 66},
    {"text": "If a bug occurs and no one writes a test for it, does it really exist?", "category": "EXISTENTIAL", "likes": 72},
    {"text": "Stack Overflow was down for 7 minutes. I wrote that code during those 7 minutes.", "category": "BLAMING OTHERS", "likes": 88},
    {"text": "I used AI to write the code. The AI used AI to test it. The test passed. Nothing works.", "category": "DEVELOPER", "likes": 99},
    {"text": "I spilled chai on my laptop. It's slower now but ironically smells better.", "category": "PHYSICAL", "likes": 44},
    {"text": "The code was in quantum superposition of working and not working. You observed it. That's on you.", "category": "EXISTENTIAL", "likes": 58},
    {"text": "A nearby black hole slightly bent spacetime around my CPU. The math just wasn't the same.", "category": "COSMIC", "likes": 35},
    {"text": "I fixed the bug. A new bug appeared. We are Sisyphus now.", "category": "EXISTENTIAL", "likes": 80},
    {"text": "The PM changed requirements while I was asleep. My dreams are now outdated.", "category": "BLAMING OTHERS", "likes": 91},
    {"text": "My keyboard has a dead zone between D and F. I typed 'efault' instead of 'default' for 3 days.", "category": "PHYSICAL", "likes": 55},
]

# ── Session state ──────────────────────────────────────────────────────────────
if "excuses"         not in st.session_state: st.session_state.excuses         = [dict(e, id=i, ai=False) for i, e in enumerate(DEFAULT_EXCUSES)]
if "next_id"         not in st.session_state: st.session_state.next_id         = len(DEFAULT_EXCUSES)
if "current_excuse"  not in st.session_state: st.session_state.current_excuse  = None
if "liked_ids"       not in st.session_state: st.session_state.liked_ids       = set()
if "total_generated" not in st.session_state: st.session_state.total_generated = 0
if "ai_tokens_used"  not in st.session_state: st.session_state.ai_tokens_used  = 0

# ── Functions ──────────────────────────────────────────────────────────────────
def get_random(category="ALL"):
    pool = [e for e in st.session_state.excuses if category == "ALL" or e["category"] == category]
    if not pool: return None
    ex = random.choice(pool)
    st.session_state.current_excuse = ex
    st.session_state.total_generated += 1
    return ex

def ai_generate(category, situation=""):
    client = Groq(api_key=GROQ_API_KEY)
    desc = {
        "DEVELOPER":      "coding, tools, git, npm, or dev environment",
        "COSMIC":         "space, physics, planets, or cosmic events",
        "PHYSICAL":       "keyboards, monitors, rubber ducks, or hardware accidents",
        "BLAMING OTHERS": "the intern, PM, designer, client, or Stack Overflow",
        "EXISTENTIAL":    "questioning reality, code existence, or the nature of bugs",
    }
    hint = f'Situation: "{situation}".' if situation.strip() else ""
    prompt = (
        f"You're a hilariously dramatic programmer. Write ONE funny excuse about {desc[category]}.\n"
        f"{hint}\nRules: 1-3 sentences, under 200 chars, no quotes, just the excuse. Be very creative and funny!"
    )
    res    = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150, temperature=0.9,
    )
    text   = res.choices[0].message.content.strip()
    tokens = res.usage.total_tokens
    st.session_state.ai_tokens_used += tokens
    new = {"id": st.session_state.next_id, "text": text, "category": category, "likes": 0, "ai": True}
    st.session_state.excuses.append(new)
    st.session_state.next_id += 1
    st.session_state.current_excuse = new
    st.session_state.total_generated += 1
    return new, tokens

def do_like(eid):
    if eid in st.session_state.liked_ids: return False
    for e in st.session_state.excuses:
        if e["id"] == eid:
            e["likes"] += 1
            st.session_state.liked_ids.add(eid)
            return True
    return False

def submit_excuse(text, category):
    new = {"id": st.session_state.next_id, "text": text.strip(),
           "category": category, "likes": 0, "ai": False, "user": True}
    st.session_state.excuses.append(new)
    st.session_state.next_id += 1

def card(excuse):
    cat  = excuse["category"]
    ai_b = ' <span class="ai-badge">✨ AI Generated</span>' if excuse.get("ai")   else ""
    us_b = ' <span class="ai-badge" style="color:#bf7fff;border-color:#bf7fff;animation:none">👤 Community</span>' if excuse.get("user") else ""
    st.markdown(f"""
    <div class="excuse-box">
        <span class="tag {TAG_CLASS.get(cat,'tag-DEVELOPER')}">{ICONS.get(cat,'💬')} {cat}</span>{ai_b}{us_b}<br/><br/>
        {excuse['text']}
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# UI
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-wrap">
  <div class="hero-corner tl"></div>
  <div class="hero-corner tr"></div>
  <div class="hero-corner bl"></div>
  <div class="hero-corner br"></div>
  <div class="hero-version">v2.0 &nbsp;&middot;&nbsp; ONLINE</div>
  <div style="line-height:1">
    <span class="big-title" data-text="EXCUSE.EXE">EXCUSE.EXE</span>
  </div>
  <p class="subtitle">// when your code breaks and you need a reason fast</p>
  <div class="hero-tags">
    <span class="hero-tag">&#x26A1; PYTHON</span>
    <span class="hero-tag">&#x1F916; GROQ AI</span>
    <span class="hero-tag">&#x1F30A; STREAMLIT</span>
    <span class="hero-tag">&#x1F602; ZERO ACCOUNTABILITY</span>
  </div>
  <div class="hero-line"></div>
</div>
""", unsafe_allow_html=True)

# Stats
c1, c2, c3, c4 = st.columns(4)
c1.metric("📦 Excuses",   len(st.session_state.excuses))
c2.metric("❤️ Likes",    sum(e["likes"] for e in st.session_state.excuses))
c3.metric("✨ AI Made",   sum(1 for e in st.session_state.excuses if e.get("ai")))
c4.metric("👤 Community", sum(1 for e in st.session_state.excuses if e.get("user")))
st.divider()

tab1, tab2, tab3, tab4 = st.tabs(["⚡ Generate", "✨ AI", "📝 Submit", "🏆 Top"])

# ── TAB 1 ─────────────────────────────────────────────────────────────────────
with tab1:
    st.subheader("Random Excuse Generator")
    opts   = ["ALL"] + CATEGORIES
    labels = ["🎲 All"] + [f"{ICONS[c]} {c}" for c in CATEGORIES]
    sel    = st.selectbox("Category", labels, key="t1_cat")
    cat    = opts[labels.index(sel)]

    if st.button("⚡  GENERATE  EXCUSE", use_container_width=True):
        if not get_random(cat):
            st.warning("No excuses in that category!")

    if st.session_state.current_excuse:
        ex = st.session_state.current_excuse
        card(ex)
        ca, cb = st.columns(2)
        with ca:
            already = ex["id"] in st.session_state.liked_ids
            if st.button(f"❤️  {ex['likes']}  {'✓ Liked' if already else 'Like'}", key=f"l1_{ex['id']}", use_container_width=True):
                if do_like(ex["id"]):
                    st.toast("❤️ Liked!", icon="❤️")
                    st.rerun()
                else:
                    st.toast("Already liked 😄")
        with cb:
            st.download_button("📥  Save .txt", data=ex["text"], file_name="excuse.txt", use_container_width=True)
        st.code(ex["text"], language=None)
    else:
        st.info("👆 Tap **GENERATE EXCUSE** to start!")

    st.caption(f"Generated this session: {st.session_state.total_generated}")

# ── TAB 2 ─────────────────────────────────────────────────────────────────────
with tab2:
    st.subheader("✨ AI Excuse Generator")
    ok = bool(GROQ_API_KEY and GROQ_API_KEY != "your_groq_api_key_here")
    if not ok:
        st.error("⚠️ No Groq API key!\n\n1. Open `.env`\n2. Set `GROQ_API_KEY=your_key`\n3. Get free key → https://console.groq.com\n4. Restart app")
    else:
        st.success("✅ Groq connected — LLaMA 3.3 70B", icon="🤖")

    ai_sel = st.selectbox("Category", [f"{ICONS[c]} {c}" for c in CATEGORIES], key="t2_cat")
    ai_cat = ai_sel.split(" ", 1)[1]
    sit    = st.text_input("Your situation (optional)", placeholder="e.g. My loop is somehow infinite AND empty", max_chars=150)

    if st.button("✨  GENERATE  WITH  GROQ  AI", use_container_width=True, disabled=not ok):
        with st.spinner("🤖 LLaMA 3 is cooking up an excuse..."):
            try:
                exc, tok = ai_generate(ai_cat, sit)
                st.toast(f"✨ Done! ({tok} tokens)", icon="🤖")
                st.rerun()
            except Exception as e:
                err = str(e)
                st.error("❌ Bad API key." if "401" in err else "⏳ Rate limit — try again!" if "429" in err else f"❌ {err}")

    ai_list = [e for e in st.session_state.excuses if e.get("ai")]
    if ai_list:
        latest = ai_list[-1]
        st.markdown("**Latest AI Excuse:**")
        card(latest)
        cl, cs = st.columns(2)
        with cl:
            a2 = latest["id"] in st.session_state.liked_ids
            if st.button(f"❤️  {latest['likes']}  {'✓ Liked' if a2 else 'Like'}", key=f"l2_{latest['id']}", use_container_width=True):
                if do_like(latest["id"]):
                    st.toast("❤️ Liked!", icon="❤️")
                    st.rerun()
                else:
                    st.toast("Already liked 😄")
        with cs:
            st.download_button("📥  Save", data=latest["text"], file_name="ai_excuse.txt", use_container_width=True)
    if st.session_state.ai_tokens_used:
        st.caption(f"Session tokens used: {st.session_state.ai_tokens_used}")

# ── TAB 3 ─────────────────────────────────────────────────────────────────────
with tab3:
    st.subheader("📝 Submit Your Excuse")
    st.markdown("Think yours is funnier? Submit it 😂")
    txt = st.text_area("Your excuse", placeholder="Type your funniest programmer excuse...", max_chars=280, height=120, key="t3_txt")
    st.caption(f"{len(txt)}/280 characters")
    cat_sel = st.selectbox("Category", [f"{ICONS[c]} {c}" for c in CATEGORIES], key="t3_cat")
    cat3    = cat_sel.split(" ", 1)[1]
    if st.button("🚀  SUBMIT  EXCUSE", use_container_width=True):
        if len(txt.strip()) < 10:
            st.error("⚠️ Too short! At least 10 characters.")
        else:
            submit_excuse(txt, cat3)
            st.success("🎉 Submitted! Check the leaderboard.")
            st.toast("🚀 Live now!", icon="🎉")
            st.balloons()

# ── TAB 4 ─────────────────────────────────────────────────────────────────────
with tab4:
    st.subheader("🏆 Top Excuses")
    f1, f2 = st.columns(2)
    with f1:
        lb_opts = ["ALL"] + CATEGORIES
        lb_lbls = ["🎲 All"] + [f"{ICONS[c]} {c}" for c in CATEGORIES]
        lb_sel  = st.selectbox("Filter", lb_lbls, key="t4_cat")
        lb_cat  = lb_opts[lb_lbls.index(lb_sel)]
    with f2:
        sort = st.selectbox("Sort", ["❤️ Most Liked", "🆕 Newest"], key="t4_sort")

    pool = [e for e in st.session_state.excuses if lb_cat == "ALL" or e["category"] == lb_cat]
    pool = sorted(pool, key=lambda e: e["likes"], reverse=True) if "Liked" in sort else list(reversed(pool))

    if not pool:
        st.info("No excuses here yet!")
    else:
        for i, ex in enumerate(pool[:15]):
            rank  = {0:"🥇",1:"🥈",2:"🥉"}.get(i, f"#{i+1}")
            extra = (" ✨" if ex.get("ai") else "") + (" 👤" if ex.get("user") else "")
            r1, r2 = st.columns([8, 2])
            with r1:
                st.markdown(f"""
                <div class="lb-item" style="animation-delay:{i*0.05}s">
                    <span style="color:#ffe600;font-size:1.1rem">{rank}</span>
                    &nbsp;
                    <span style="color:#6060a0;font-size:0.68rem">{ICONS.get(ex['category'],'💬')} {ex['category']}{extra}</span><br/>
                    <span style="font-size:clamp(0.8rem,3vw,0.9rem);color:#e0e0f0">{ex['text']}</span>
                </div>""", unsafe_allow_html=True)
            with r2:
                if st.button(f"❤️ {ex['likes']}", key=f"l4_{ex['id']}", use_container_width=True):
                    if do_like(ex["id"]):
                        st.toast("❤️ Liked!", icon="❤️")
                        st.rerun()
                    else:
                        st.toast("Already liked 😄")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<p style='text-align:center;color:#3a3a5c;font-family:monospace;font-size:0.72rem'>"
    "Built with Python + Streamlit + Groq AI 🤖 | No programmers were held accountable 😂"
    "</p>", unsafe_allow_html=True
)