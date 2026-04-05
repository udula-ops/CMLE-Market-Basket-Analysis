# 🛒 Market Basket Analysis — Capstone Project

**Silver Badge | Association Rule Learning**
Dataset: UCI Online Retail II (UK Only)

---

## 📌 Project Overview

This project applies **Association Rule Learning** to discover product purchasing patterns from a real-world UK online retail dataset. Two algorithms are implemented and compared — **Apriori** and **FP-Growth** — and the best model is deployed as an interactive **Streamlit web application**.

---

## 📁 File Structure

```
YourName_YourWhatsappNum/
├── Notebooks/
│   ├── 01_data_preprocessing.ipynb   ← Data cleaning & encoding
│   └── 02_model_development.ipynb    ← Apriori & FP-Growth training
├── Application/
│   ├── MBR App.py                    ← Streamlit recommender app
│   ├── model/
│   │   └── fpgrowth_rules.pkl        ← Saved FP-Growth rules
│   └── requirements.txt              ← Python dependencies
├── Dataset/
│   └── online_retail_II.csv          ← Raw dataset (UCI)
└── Video_Demo/
    └── YourName_demo.mp4             ← Screen recording demo
```

---

## 🔧 Setup & Installation

### 1. Clone or download this project

### 2. Install dependencies
```bash
py -m pip install -r Application/requirements.txt
```

### 3. Run the Streamlit app
```bash
cd Market Basket Analysis Application
py -m streamlit run MBR App.py
```

---

## 📊 Dataset

| Property | Detail |
|---|---|
| Source | UCI Machine Learning Repository |
| File | `online_retail_II.csv` |
| Original rows | 1,067,371 |
| After cleaning (UK only) | ~725,250 |
| Unique transactions | 33,541 |
| Unique products | 5,206 |

**Cleaning steps applied:**
- Removed rows with missing `CustomerID` or `Description`
- Removed cancelled orders (Invoice starting with `C`)
- Removed rows with `Quantity ≤ 0` or `Price ≤ 0`
- Filtered to **United Kingdom** only

---

## 🤖 Models

### Model 1 — Apriori (`apyori`)

| Parameter | Value |
|---|---|
| min_support | 0.01 |
| min_confidence | 0.2 |
| min_lift | 1 |
| min_length | 2 |

| Result | Value |
|---|---|
| Training Time | 0.00 sec |
| Rules Generated | 371 |
| Avg Confidence | 0.4284 |
| Avg Lift | 13.5473 |
| Max Lift | 59.3920 |

---

### Model 2 — FP-Growth (`mlxtend`) ⭐ Best Model

| Parameter | Value |
|---|---|
| min_support | 0.01 |
| min_threshold | 1 |

| Result | Value |
|---|---|
| Training Time | 56.59 sec |
| Rules Generated | 398 |
| Avg Confidence | 0.3941 |
| Avg Lift | 12.6258 |
| Max Lift | 57.0593 |

**Why FP-Growth was selected:**
- More rules generated (398 vs 371)
- Returns a clean `pandas` DataFrame — ideal for Streamlit integration
- Industry-standard for large-scale basket analysis

---

## 🖥️ Web Application

The Streamlit app (`MBR App.py`) allows users to:

1. Select any product from a dropdown (auto-populated from rules)
2. Choose how many recommendations to display (1–20)
3. View a ranked table of recommended products with **Confidence**, **Lift**, and **Support**
4. Visualise scores via interactive bar charts

**Key metrics explained:**
- **Support** — How often the product pair appears together
- **Confidence** — How likely the recommended item is bought when the selected item is in the basket
- **Lift** — How much more likely the pair occurs vs random chance (>1 = positive association)

---

## 📦 Dependencies

```
streamlit
pandas
joblib
mlxtend
apyori
openpyxl
scikit-learn
```

---

## 🎓 Academic Info

| Field | Detail |
|---|---|
| Project Type | Capstone Project |
| Badge | Silver |
| Topic | Association Rule Learning |
| Tools | Google Colab, Python, Streamlit |
| Deadline | April 6, 2026 — 1PM Sri Lanka Time |
