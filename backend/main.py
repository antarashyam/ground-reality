import requests
import os
from dotenv import load_dotenv

load_dotenv()

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

def get_top_news():
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "economy layoffs jobs tech",
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY,
        "pageSize": 1
    }
    response = requests.get(url, params=params)
    article = response.json()["articles"][0]
    return f"{article['title']}. {article['description']}"

def get_unemployment_rate():
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": "UNRATE",
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "limit": 1,
        "sort_order": "desc"
    }
    response = requests.get(url, params=params)
    latest = response.json()["observations"][0]
    return f"US unemployment: {latest['value']}% as of {latest['date']}"

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

def explain_for_student(news, economic_context, skill_counts):
    skill_summary = "\n".join([f"- {s}: {c} jobs" for s, c in skill_counts.items()])
    
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    prompt = f"""
    You are an honest economic advisor speaking to a 3rd year Computer Science student in India.
    
    Recent economic news: {news}
    
    Current economic context: {economic_context}
    
    Live job market demand in India right now:
    {skill_summary}
    
    Based on all of this, explain in plain language:
    1. What's happening in the economy and why it matters
    2. Which skills are actually in demand right now vs overhyped
    3. What this means specifically for a CS student in India
    4. One concrete action they should take this week
    
    Be honest and direct. No corporate speak. Under 200 words.
    """
    body = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=body)
    return response.json()["content"][0]["text"]

# Run everything
print("Fetching data...\n")
news = get_top_news()
economic_context = get_unemployment_rate()
skill_counts = get_skill_counts()
explanation = explain_for_student(news, economic_context, skill_counts)

print("📰 NEWS:", news)
print("\n📊 ECONOMIC CONTEXT:", economic_context)
print("\n📈 SKILL DEMAND:")
for skill, count in sorted(skill_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"   {skill}: {count:,} jobs")
print("\n🎓 WHAT THIS MEANS FOR YOU:")
print(explanation)