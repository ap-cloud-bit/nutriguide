-- NutriGuide PostgreSQL Schema
-- Run this on Supabase SQL Editor or any PostgreSQL instance

-- Users
CREATE TABLE IF NOT EXISTS users (
    user_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email         TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    age           INT,
    gender        TEXT,
    height_cm     INT,
    weight_kg     FLOAT,
    budget_level  TEXT CHECK (budget_level IN ('low','medium','high')) DEFAULT 'medium',
    goal          TEXT DEFAULT 'balanced',
    preferences   TEXT[] DEFAULT '{}',
    allergies     TEXT[] DEFAULT '{}',
    created_at    TIMESTAMP DEFAULT now(),
    updated_at    TIMESTAMP DEFAULT now()
);

-- Pantry Items
CREATE TABLE IF NOT EXISTS pantry_items (
    item_id     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID REFERENCES users(user_id) ON DELETE CASCADE,
    name        TEXT NOT NULL,
    quantity    INT DEFAULT 1,
    unit        TEXT,
    detected_at TIMESTAMP DEFAULT now()
);

-- Food Items (cached from Open Food Facts)
CREATE TABLE IF NOT EXISTS food_items (
    food_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    barcode      TEXT UNIQUE NOT NULL,
    product_name TEXT,
    brand        TEXT,
    nutriscore   TEXT,
    nova_group   INT,
    ingredients  TEXT,
    image_url    TEXT,
    last_fetched TIMESTAMP DEFAULT now()
);

-- Food Safety Scores
CREATE TABLE IF NOT EXISTS food_safety_scores (
    safety_id    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    barcode      TEXT REFERENCES food_items(barcode) ON DELETE CASCADE,
    health_score FLOAT CHECK (health_score BETWEEN 0 AND 10),
    upf_score    INT CHECK (upf_score BETWEEN 1 AND 4),
    ai_analysis  TEXT,
    last_scanned TIMESTAMP DEFAULT now()
);

-- Meal Plans
CREATE TABLE IF NOT EXISTS meal_plans (
    plan_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id       UUID REFERENCES users(user_id) ON DELETE CASCADE,
    duration_days INT,
    plan_text     TEXT,
    estimated_cost TEXT,
    goal          TEXT,
    budget_level  TEXT,
    created_at    TIMESTAMP DEFAULT now()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_pantry_user ON pantry_items(user_id);
CREATE INDEX IF NOT EXISTS idx_plans_user  ON meal_plans(user_id);
CREATE INDEX IF NOT EXISTS idx_food_barcode ON food_safety_scores(barcode);
