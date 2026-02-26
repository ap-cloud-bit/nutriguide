# 🚀 NutriGuide — Complete Deployment Guide (Beginner Friendly)

Follow these steps in order. Each step takes about 5–10 minutes.

---

## STEP 1 — Get Your API Key (Free)

1. Go to https://console.anthropic.com
2. Sign up with your email
3. Go to "API Keys" → click "Create Key"
4. Copy the key — it starts with `sk-ant-...`
5. Keep it safe — you'll need it in Step 3

---

## STEP 2 — Push to GitHub

1. Go to https://github.com → click "New Repository"
2. Name it: `nutriguide`
3. Keep it Public (so employers can see it)
4. Click "Create repository"

Then in your terminal (inside the nutriguide folder):
```bash
git init
git add .
git commit -m "🥦 Initial NutriGuide commit — AI Food Intelligence Agent"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/nutriguide.git
git push -u origin main
```

---

## STEP 3 — Deploy Backend to Railway (Free)

1. Go to https://railway.app → Sign up with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your `nutriguide` repo
4. Set Root Directory to: `backend`
5. Railway will detect the Dockerfile automatically

**Add Environment Variables:**
Click your service → "Variables" tab → Add:
- `ANTHROPIC_API_KEY` = your key from Step 1
- `SECRET_KEY` = any random string (e.g. `nutriguide-prod-2026`)

6. Click "Deploy" — wait 2 minutes
7. Go to "Settings" → "Networking" → "Generate Domain"
8. Copy your URL — it looks like: `https://nutriguide-api.railway.app`

---

## STEP 4 — Update Frontend with Your Backend URL

Open `frontend/index.html` in any text editor.

Find this line (near the top of the `<script>` section):
```js
const API_BASE = 'http://localhost:8000';
```

Change it to your Railway URL:
```js
const API_BASE = 'https://nutriguide-api.railway.app';
```

Save the file, then commit and push:
```bash
git add frontend/index.html
git commit -m "Update API_BASE to Railway deployment URL"
git push
```

---

## STEP 5 — Deploy Frontend to Vercel (Free)

1. Go to https://vercel.com → Sign up with GitHub
2. Click "Add New Project" → Import your `nutriguide` repo
3. Set Root Directory to: `frontend`
4. Click "Deploy"
5. Wait 1 minute — your app is live! 🎉

Vercel gives you a URL like: `https://nutriguide.vercel.app`

---

## STEP 6 — Test Your Live App

Open your Vercel URL and try:

1. **Scan Tab** → Enter barcode `3017620422003` → click Scan
   - You should see Nutella's health score and AI analysis

2. **Plan Tab** → Select "Fat Loss" + "Low" budget → Generate Plan
   - Claude generates a full 7-day meal plan

3. **Chat Tab** → Ask "Is oat milk healthier than dairy?"
   - NutriGuide responds with a detailed answer

---

## OPTIONAL: Add Free Database (Supabase)

1. Go to https://supabase.com → Create free account
2. Create new project → choose any region
3. Go to "SQL Editor" → paste contents of `backend/models/schema.sql` → Run
4. Go to "Settings" → "Database" → copy "Connection string (URI)"
5. Add to Railway environment variables:
   - `DATABASE_URL` = your Supabase connection string

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Could not connect to backend" | Check Railway deployment logs; verify ANTHROPIC_API_KEY is set |
| "Product not found" | Try a different barcode from openfoodfacts.org |
| "AI analysis unavailable" | Your ANTHROPIC_API_KEY is missing or incorrect |
| Frontend shows blank page | Open browser console (F12) and check for errors |

---

## ✅ Final Checklist

- [ ] Code pushed to GitHub (public repo)
- [ ] Backend deployed on Railway with API key
- [ ] Frontend deployed on Vercel pointing to Railway URL
- [ ] Tested food scan, meal plan, and chat
- [ ] LinkedIn post published with GitHub + demo links
- [ ] GitHub repo has good description and topics set

Congratulations! You've shipped a real AI product. 🥦🎉
