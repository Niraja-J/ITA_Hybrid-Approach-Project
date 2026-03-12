# ITA_Hybrid-Approach-Project
Niraja J, IPM06123_ Sec B_ Risk Map AI
# 🌍 RiskMap AI
### AI-Powered Geopolitical Risk & Investment Intelligence Platform

> Predicts country-level geopolitical risk 1–5 years ahead using machine learning, real-time news NLP, and company-specific exposure analysis.

---

## 🔴 Live Dashboard
👉 **[Click here to open RiskMap AI](https://itahybrid-approach-project-megkzuh2vadkkwhioaqt9w.streamlit.app/)**

### Login Credentials
| Company | Password |
|---|---|
| AWS | aws2026 |
| NVIDIA | nvidia2026 |
| Microsoft | msft2026 |

---

## 📌 What This System Does
- Forecasts geopolitical risk for 263 countries from 2025 to 2029
- Trained on 20 years of World Bank + UCDP conflict data
- Updates risk scores using live BBC & Reuters news headlines
- Generates company-specific risk scores for AWS, NVIDIA, and Microsoft
- Recommends investment allocation based on risk-adjusted opportunity scores
- Simulates what-if scenarios like trade wars and conflict escalations

---

## 🗂️ Repository Structure
| File | Description |
|---|---|
| `streamlit_app.py` | Main dashboard application |
| `riskmap_ai.ipynb` | Complete data pipeline + ML model |
| `final_predictions.csv` | 5-year forecast data (2025–2029) |
| `news_headlines.csv` | Live news risk signals |
| `ai_risk_ml_results.csv` | ML model results |
| `requirements.txt` | Python dependencies |

---

## 🤖 Model Performance
| Model | Train R² | Test R² |
|---|---|---|
| Gradient Boosting | 0.996 | 0.664 |
| Random Forest | 0.974 | 0.674 |

**Best model: Random Forest (selected on test performance)**

Top predictors: Political Stability (68.5%) · Conflict Deaths (8.5%) · Conflict Intensity (8.2%)

---

## 🛠️ Tech Stack
Python · Scikit-learn · ARIMA · Streamlit · Plotly · World Bank Data · UCDP
