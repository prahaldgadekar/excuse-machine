<div align="center">

<!-- Animated wave header banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=00ff88&height=180&section=header&text=EXCUSE.EXE&fontSize=70&fontColor=0a0a0f&fontAlignY=38&desc=Python%20Streamlit%20Edition&descAlignY=60&descColor=0a0a0f&animation=fadeIn" width="100%"/>

<!-- Animated typewriter subtitle -->
<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&size=18&duration=3000&pause=1000&color=00FF88&center=true&vCenter=true&multiline=true&repeat=true&width=600&height=60&lines=A+funny+programmer+excuse+machine+🤖;Built+with+pure+Python+🐍;No+HTML+·+No+CSS+·+No+JavaScript+😎;Zero+Accountability+Guaranteed+😂" alt="Typing SVG"/>

<br/>

<!-- Live demo big button -->
<a href="https://excuse-machine-s9zrufbo4rlgcy4tzeffah.streamlit.app/">
  <img src="https://img.shields.io/badge/🚀%20LIVE%20DEMO-Try%20It%20Now-FF4B4B?style=for-the-badge" alt="Live Demo"/>
</a>

<br/><br/>

<!-- Tech badges -->
<img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat-square&logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/Claude_API-Anthropic-D97706?style=flat-square"/>
<img src="https://img.shields.io/badge/Accountability-Zero%20😂-00C853?style=flat-square"/>

</div>

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| 🐍 Language | Python 3.8+ |
| 🌊 UI / Web | Streamlit |
| 🤖 AI | Anthropic Claude API |
| 🔑 Config | python-dotenv (`.env` file) |

---

## 📁 Project Structure

```
excuse-streamlit/
├── app.py               ← All Python code (UI + logic)
├── requirements.txt     ← pip dependencies
├── .env                 ← Your API key (DO NOT commit!)
├── .env.example         ← Safe template to commit
├── .gitignore           ← Ignores .env automatically
└── .streamlit/
    └── config.toml      ← Dark theme config
```

---

## 🚀 Setup — 4 Steps

### Step 1 — Check Python version
```bash
python --version   # Should be 3.8 or higher
```

### Step 2 — Install dependencies
```bash
cd excuse-streamlit
pip install -r requirements.txt
```

### Step 3 — Add your API key

Open `.env` and replace the placeholder:
```
ANTHROPIC_API_KEY=your_real_key_here
```
> 🔗 Get your key at: https://console.anthropic.com

### Step 4 — Run the app
```bash
streamlit run app.py
```
> 🌐 Browser opens automatically at **http://localhost:8501**

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| ⚡ Random Generate | Pick from 20+ pre-loaded excuses |
| 🎲 Category Filter | `DEVELOPER` · `COSMIC` · `PHYSICAL` · `BLAMING OTHERS` · `EXISTENTIAL` |
| ✨ AI Generate | Claude creates a brand new excuse just for you |
| 🎯 Situation Input | Tell Claude your situation for a targeted excuse |
| ❤️ Like System | Upvote your favourite excuses |
| 📝 Submit Yours | Add your own funny excuse to the pool |
| 🏆 Leaderboard | Top 15 excuses sorted by likes |
| 📥 Save as .txt | Download any excuse to your machine |

---

## 🔐 API Key Security

- ✅ Key stored in `.env` — never hardcoded in source
- ✅ `.gitignore` prevents `.env` from being pushed to GitHub
- ✅ `.env.example` is a safe, key-free template to commit

> ⚠️ **Never share your `.env` file or paste your API key publicly.**  
> If you accidentally push it, rotate it immediately at [console.anthropic.com](https://console.anthropic.com).

---

## 💡 Extend Ideas

| Idea | How |
|------|-----|
| 🗄️ Persistent storage | Save excuses with `sqlite3` (Python built-in) |
| ☁️ Free deployment | Deploy on [Streamlit Cloud](https://streamlit.io/cloud) |
| 🔊 Voice readout | Add TTS with `pyttsx3` |
| 📊 Export data | Download leaderboard as CSV |

---

## 🧑‍💻 Author

**Prahlad Gadekar**

[![GitHub](https://img.shields.io/badge/GitHub-prahaldgadekar-181717?style=flat-square&logo=github)](https://github.com/prahaldgadekar)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-prahladgadekar-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/prahladgadekar)

---

<!-- Animated footer wave -->
<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=00ff88&height=100&section=footer&animation=fadeIn" width="100%"/>
  <sub>Built with Python · Streamlit · Anthropic Claude API · python-dotenv</sub><br>
  <sub>Made with ❤️ and zero accountability 😂</sub>
</div>
