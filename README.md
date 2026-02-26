<div align="center">

<img src="https://img.shields.io/badge/🥦-NutriGuide-2ECC71?style=for-the-badge&labelColor=1F5133" alt="NutriGuide"/>

# NutriGuide — AI Food Intelligence Agent

**Scan food. Plan meals. Optimize your budget. Powered by Claude AI.**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Claude AI](https://img.shields.io/badge/Claude-Haiku-D97706?style=flat-square&logo=anthropic&logoColor=white)](https://anthropic.com)
[![Open Food Facts](https://img.shields.io/badge/Open%20Food%20Facts-6M%2B%20Products-E63E11?style=flat-square)](https://openfoodfacts.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-2ECC71?style=flat-square)](LICENSE)
[![Deploy on Railway](https://img.shields.io/badge/Deploy-Railway-7B2FBE?style=flat-square&logo=railway&logoColor=white)](https://railway.app)

[**Live Demo**](https://nutriguide.vercel.app) · [**API Docs**](https://nutriguide-api.railway.app/docs) · [**Report Bug**](https://github.com/ap-cloud-bit/nutriguide/issues)

</div>

---

## 🎯 What is NutriGuide?

NutriGuide is a full-stack AI food intelligence agent that solves a real problem: **73% of consumers struggle to interpret food labels**, and ultra-processed food consumption keeps rising despite widespread health concerns *(PwC Voice of the Consumer 2025)*.

NutriGuide closes this gap by combining:
- 🗄️ **Open Food Facts** — the world's largest open food database (6M+ products, free)
- 🤖 **Claude AI (Anthropic)** — for intelligent, context-aware nutrition analysis
- 📊 **NOVA + Nutri-Score** — the same evidence-based frameworks used by European health authorities

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📷 **Food Scanner** | Enter any barcode → instant health score (0–10), UPF rating, AI analysis |
| 📋 **Meal Planner** | AI-generated 7-day meal plans based on your goal, budget & pantry |
| 🛒 **Cart Optimizer** | Submit your shopping list → get healthier, cheaper alternatives |
| 💬 **AI Nutritionist** | Conversational chat with NutriGuide — ask anything about food |
| 👤 **User Profiles** | Personalized plans based on age, goals, allergies, preferences |

---

## 🏗️ Architecture

```
nutriguide/
│
├── backend/                    # Python REST API (FastAPI)
│   ├── main.py                 # App entry point + CORS + routing
│   ├── Dockerfile              # Container config for deployment
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Environment variable template
│   │
│   ├── core/
│   │   ├── config.py           # Reads .env — API keys, DB URL
│   │   └── ai_client.py        # Claude AI client + all prompts
│   │
│   ├── routes/
│   │   ├── food.py             # POST /food/scan
│   │   ├── mealplan.py         # POST /mealplan/generate
│   │   ├── ai_chat.py          # POST /ai/chat
│   │   ├── shopping.py         # POST /shopping/optimize-cart
│   │   └── user.py             # POST /user/create · GET /user/{id}
│   │
│   └── models/
│       ├── schemas.py          # Pydantic request/response models
│       └── schema.sql          # PostgreSQL schema (Supabase-ready)
│
├── frontend/
│   └── index.html              # Full app UI — no build step needed
│
├── docs/
│   ├── DEPLOYMENT_GUIDE.md     # Step-by-step Railway + Vercel + Supabase
│   └── LINKEDIN_POST.md        # Ready-to-post LinkedIn content
│
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions — auto test on every push
│
├── docker-compose.yml          # One-command local development
├── .gitignore
└── README.md
```

**Data flow:**
```
Browser → frontend/index.html
       → POST /food/scan (FastAPI)
       → Open Food Facts API (free, no key)
       → Claude AI (health analysis)
       → JSON response with score + AI insight
       → Rendered in UI
```

---

## ⚡ Quick Start

### Prerequisites
- Python 3.12+
- Anthropic API key → [Get one free](https://console.anthropic.com)

### Option A — Run Locally (Recommended for beginners)

```bash
# 1. Clone
git clone https://github.com/ap-cloud-bit/nutriguide.git
cd nutriguide/backend

# 2. Virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Open .env and add your ANTHROPIC_API_KEY

# 5. Start the API
uvicorn main:app --reload
```

Open `frontend/index.html` in your browser. That's it — the app is running.

- **API:** http://localhost:8000
- **Interactive API docs:** http://localhost:8000/docs

### Option B — Docker (One command)

```bash
# Copy and fill in your API key
cp backend/.env.example .env
# Edit .env → add ANTHROPIC_API_KEY

# Start everything
docker-compose up
```

---

## 📡 API Reference

### `POST /food/scan`
Scan a food product by barcode.

```bash
curl -X POST http://localhost:8000/food/scan \
  -H "Content-Type: application/json" \
  -d '{"barcode": "3017620422003"}'
```

```json
{
  "product_name": "Nutella",
  "brand": "Ferrero",
  "health_score": 2.5,
  "upf_level": 4,
  "nutriscore": "E",
  "calories_100g": 539,
  "protein_100g": 6.3,
  "sugar_100g": 56.3,
  "ai_analysis": "🔴 Nutella scores 2.5/10...",
  "alternatives": ["Natural almond butter", "Unsweetened peanut butter"]
}
```

**Test barcodes:**
| Barcode | Product |
|---------|---------|
| `3017620422003` | Nutella |
| `5000159484763` | Kit Kat |
| `0038000138690` | Kellogg's Corn Flakes |
| `8710398525406` | Quaker Oats |

---

### `POST /mealplan/generate`

```bash
curl -X POST http://localhost:8000/mealplan/generate \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "fat-loss",
    "budget_level": "low",
    "duration_days": 7,
    "allergies": ["peanuts"],
    "pantry_items": ["eggs", "rice", "spinach"]
  }'
```

---

### `POST /ai/chat`

```bash
curl -X POST http://localhost:8000/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Is oat milk healthier than dairy milk?"}
    ]
  }'
```

---

### `POST /shopping/optimize-cart`

```bash
curl -X POST http://localhost:8000/shopping/optimize-cart \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"name": "Nutella", "quantity": "1 jar"},
      {"name": "White bread", "quantity": "1 loaf"}
    ],
    "budget_level": "medium"
  }'
```

> **Full interactive docs at `/docs`** — FastAPI generates a Swagger UI automatically.

---

## 🌐 Deployment

### Backend → Railway (Free tier)

1. Go to [railway.app](https://railway.app) → connect GitHub
2. New Project → Deploy from repo → set root to `backend/`
3. Add environment variables:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   SECRET_KEY=your-random-secret-string
   ```
4. Railway detects the `Dockerfile` and deploys automatically
5. Settings → Networking → Generate Domain → copy your URL

### Frontend → Vercel (Free tier)

1. Go to [vercel.com](https://vercel.com) → import repo
2. Set root directory to `frontend/`
3. Before deploying, update line in `frontend/index.html`:
   ```js
   const API_BASE = 'https://YOUR-APP.railway.app';
   ```
4. Deploy → your app is live

### Database → Supabase (Free tier, optional)

1. Create project at [supabase.com](https://supabase.com)
2. SQL Editor → paste `backend/models/schema.sql` → Run
3. Copy connection string → add to Railway as `DATABASE_URL`

---

## 🔑 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | ✅ Yes | From [console.anthropic.com](https://console.anthropic.com) |
| `DATABASE_URL` | ❌ Optional | PostgreSQL URI (Supabase). Omit to use in-memory storage. |
| `SECRET_KEY` | ❌ Optional | Any random string — used for JWT in production |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **AI** | Claude Haiku (Anthropic) | Food intelligence, meal planning, chat |
| **Backend** | FastAPI + Python 3.12 | Async REST API |
| **Food Data** | Open Food Facts API | 6M+ products, free, no key required |
| **Frontend** | HTML / CSS / JavaScript | Zero-build UI, instant deploy |
| **Database** | PostgreSQL (Supabase) | User profiles, scan history |
| **Containers** | Docker + Compose | Consistent dev/prod environments |
| **Deployment** | Railway + Vercel | Free tiers, auto-deploy from GitHub |
| **CI/CD** | GitHub Actions | Auto-test on every push |

---

## 📊 The Problem This Solves

*(Based on PwC Voice of the Consumer 2025)*

- **73%** of consumers can't interpret food labels
- **68%** are concerned about ultra-processed foods — yet consumption keeps rising
- Average household wastes **25%** of grocery budget
- **3.6 channels** used per shopper — fragmented and confusing

NutriGuide unifies food data, AI analysis, and budget optimization into one tool.

**Target outcomes:**
- 🎯 Reduce grocery cost by 15–35%
- 🎯 Reduce UPF purchases by 20%
- 🎯 Reduce pantry waste by 25%

---

## 🗺️ Roadmap

- [x] Barcode food scanner with health scoring
- [x] AI-powered meal plan generation
- [x] Shopping cart optimizer
- [x] Conversational AI nutritionist
- [x] Docker deployment config
- [ ] Camera-based barcode scanning (mobile)
- [ ] Pantry photo scanning (vision AI)
- [ ] Price comparison across retailers
- [ ] Wearables integration (Fitbit, Apple Health)
- [ ] GLP-1 specific meal planning
- [ ] React Native mobile app

---

## 🤝 Contributing

Contributions are welcome. Please open an issue first to discuss what you'd like to change.

```bash
# Fork → Clone → Create branch → Make changes → Push → Open PR
git checkout -b feature/your-feature-name
```

---

## 📄 License

MIT License — free to use, modify, and distribute. See [LICENSE](LICENSE).

---

## 👤 Author

**Awais Shakeel Pasha**

AI Product Builder · DHL PK

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/your-profile)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat-square&logo=github)](https://github.com/ap-cloud-bit)

---

<div align="center">
Built with 🥦 and <a href="https://anthropic.com">Claude AI</a>
<br><br>
<i>If this project helped you, please ⭐ star the repo!</i>
</div>
