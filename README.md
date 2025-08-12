<!-- ============================================================
     README: High-Impact AI/ML Project (Animated + UI/UX Focus)
     Files expected in repo: assets/banner.gif, assets/demo_heart.gif,
     assets/demo_gdp.gif, assets/screenshot1.png
   ============================================================ -->

# 🚀 CardioAI & GDP Dashboard — AI × Beautiful UI/UX ✨

<p align="center">
  <!-- Hero animated banner (use GIF or APNG) -->
  <img src="assets/banner.gif" alt="CardioAI + GDP Banner" width="1100"/>
</p>

<p align="center">
  <a href="https://heart-diseaseprediction-zhl7t64qx8w9h5zna3vrce.streamlit.app/" target="_blank">🔥 Live Demo — Heart Disease Predictor</a> &nbsp; • &nbsp;
  <a href="https://gdpdashboard-gprvxni7fdy2iaqfuynn7i.streamlit.app/" target="_blank">🌍 Live Demo — GDP Dashboard</a>
</p>

<p align="center">
  <!-- Badges (customize username/repo) -->
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/ML-RandomForest-4C1?style=for-the-badge" alt="ML"/>
  <img src="https://img.shields.io/badge/Live-Demo-green?style=for-the-badge" alt="Live"/>
</p>

---

## ⚡ TL;DR — Why this repo = instant scroll stopper
- **Interactive, deployable Streamlit apps** that transform raw data into beautiful, explorable visuals.  
- **AI model** (Heart disease prediction) + **Economic visualizer** (GDP trends).  
- UX-first design: animations, crisp charts, clear CTAs, bilingual support options.  
- Ready-to-demo — share live links, short GIFs, and a slick README = recruiter magnet.

---

## ✨ Animated Demos (copy these filenames into `assets/`)
<p align="center">
  <img src="assets/demo_heart.gif" alt="Heart Demo" width="520"/>&nbsp;&nbsp;
  <img src="assets/demo_gdp.gif" alt="GDP Demo" width="520"/>
</p>

> **File names expected** (put these in `/assets`):  
> `banner.gif`, `demo_heart.gif`, `demo_gdp.gif`, `screenshot1.png`, `screenshot2.png`, `screenshot3.png`

---

## 🔎 Feature Highlights
- **Heart Disease Predictor**
  - Fast inference with a RandomForest classifier
  - SHAP-based explainability (feature impact)
  - Clear probability + confidence UI
- **GDP Dashboard**
  - Country comparators, year-range sliders, export CSV
  - Interactive Plotly charts (zoom/pan)
- **UX/Accessibility**
  - Responsive layout, Hindi/English labels option, color-blind safe palettes
  - Local processing — no user data is stored

---

## 🎨 UI / UX DESIGN GUIDE (colors, fonts, animations)
Use these to keep a consistent *brand/professional* look.

**Primary palette**
- Accent Blue: `#0077CC`  
- Deep Teal: `#005f73`  
- Action Red: `#ff4b4b`  
- Soft Gray (background cards): `#f6f8fa`  
- Text: `#0b1220`

**Fonts (for banner/design assets / web)**
- Headline: *Poppins / Inter*  
- Body: *Roboto / Open Sans*

**Animation suggestions**
- Hero banner: subtle left→right parallax + glowing title (GIF or APNG)  
- Demo GIFs: screen-record 6–12s loops showing the main flow (LICEcap / ScreenToGif / Record with OBS → trim)  
- Micro animations: progress bars / metric counters (use streamlit-animation libs or Lottie)

---

## 📸 How to create the assets (quick)
- **Banner (animated):** Figma or Canva — create 1200×400 px canvas, animate text + icons, export as GIF/APNG.  
- **Demo GIFs:** Use `ScreenToGif` (Windows) or `Peek` (Linux) to capture the app flow (6–10s), crop & optimize with `ezgif.com`.  
- **Optimize images**: TinyPNG or Squoosh — keep each < 2MB for fast GitHub load.

---

## 🧭 Installation & Run (local dev)
```bash
# clone
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# recommended: create venv
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# install
pip install -r requirements.txt

# run one of the apps (example)
streamlit run src/heart_app.py
# or
streamlit run src/gdp_app.py

