from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
FRED_API_KEY = os.getenv("FRED_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_API_KEY = os.getenv("ADZUNA_API_KEY")

SKILLS = [
    "machine learning", "react", "cloud computing",
    "python", "data science", "cybersecurity",
    "devops", "artificial intelligence"
]

def get_news(count=30):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "economy jobs tech layoffs hiring AI india",
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY,
        "pageSize": count
    }
    response = requests.get(url, params=params)
    articles = response.json()["articles"]
    return [{"title": a["title"], "description": a["description"], "url": a["url"], "source": a["source"]["name"], "publishedAt": a["publishedAt"]} for a in articles]

def get_economic_indicators():
    # World Bank indicators for India
    wb_indicators = {
        "SL.UEM.TOTL.ZS": ("Unemployment Rate", "%"),
        "FP.CPI.TOTL.ZG": ("Inflation Rate", "%"),
        "NY.GDP.MKTP.KD.ZG": ("GDP Growth", "%"),
    }
    results = []
    for code, (label, unit) in wb_indicators.items():
        url = f"https://api.worldbank.org/v2/country/IN/indicator/{code}?format=json&mrv=2"
        response = requests.get(url)
        data = response.json()
        obs = [o for o in data[1] if o["value"] is not None]
        if len(obs) >= 2:
            current = round(float(obs[0]["value"]), 2)
            previous = round(float(obs[1]["value"]), 2)
            change = round(current - previous, 2)
            results.append({
                "label": label,
                "value": current,
                "unit": unit,
                "change": change,
                "date": obs[0]["date"]
            })

    # Keep Fed rate from FRED since it affects India too
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": "FEDFUNDS",
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "limit": 2,
        "sort_order": "desc"
    }
    response = requests.get(url, params=params)
    obs = response.json()["observations"]
    current = float(obs[0]["value"])
    previous = float(obs[1]["value"])
    results.append({
        "label": "US Fed Rate (FRED)",
        "value": current,
        "unit": "%",
        "change": round(current - previous, 3),
        "date": obs[0]["date"]
    })

    return results

def get_skill_counts():
    results = {}
    for skill in SKILLS:
        url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
        params = {
            "app_id": ADZUNA_APP_ID,
            "app_key": ADZUNA_API_KEY,
            "what": skill,
            "results_per_page": 1
        }
        response = requests.get(url, params=params)
        results[skill] = response.json().get("count", 0)
    return results

def get_explanation(news, economic_context, skill_counts):
    skill_summary = "\n".join([f"- {s}: {c} jobs" for s, c in skill_counts.items()])
    news_summary = "\n".join([f"- {a['title']}" for a in news])
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    prompt = f"""
    You are an honest economic advisor speaking to a 3rd year Computer Science student in India.
    Recent economic news:
    {news_summary}
    Current economic context: {economic_context}
    Live job postings in India mentioning each skill (note: one posting can mention multiple skills):
    {skill_summary}
    Based on all of this, explain in plain language:
    1. What's happening in the economy and why it matters
    2. Which skills appear most in job postings right now — note these are posting counts, not a direct measure of supply vs demand
    3. What this means specifically for a CS student in India right now
    4. One concrete action they should take this week

    Important rules:
- Be honest and direct
- No corporate speak
- Do not claim Python is "universally required" — say it "appears most frequently in postings data"
- Do not claim generalists are struggling vs specialists — the data doesn't measure that
- Do not make supply/demand balance claims — you only have demand-side data
- Stick to what the numbers actually show
- Under 200 words
    """
    body = {
        "model": "claude-sonnet-4-6",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=body)
    return response.json()["content"][0]["text"]

# Separate fast endpoints
@app.route("/api/news")
def news():
    return jsonify(get_news())

@app.route("/api/context")
def context():
    return jsonify(get_economic_indicators())

@app.route("/api/skills")
def skills():
    return jsonify(get_skill_counts())

@app.route("/")
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory('../frontend', filename)

@app.route("/api/explanation")
def explanation():
    news_data = get_news()
    economic_context = str(get_economic_indicators())
    skill_counts = get_skill_counts()
    return jsonify({"explanation": get_explanation(news_data, economic_context, skill_counts)})

if __name__ == "__main__":
    app.run(debug=True)