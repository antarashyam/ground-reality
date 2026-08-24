import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")

def get_economic_news():
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "economy layoffs jobs tech",
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    for article in data["articles"][:5]:
        print(article["title"])
        print(article["description"])
        print("---")

get_economic_news()

def get_unemployment_rate():
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": "UNRATE",      # US unemployment rate
        "api_key": os.getenv("FRED_API_KEY"),
        "file_type": "json",
        "limit": 12,                 # last 12 months
        "sort_order": "desc"
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    for obs in data["observations"]:
        print(f"{obs['date']}: {obs['value']}%")

get_unemployment_rate()

def get_tech_jobs(skill):
    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"  # 'in' for India
    params = {
        "app_id": os.getenv("ADZUNA_APP_ID"),
        "app_key": os.getenv("ADZUNA_API_KEY"),
        "what": skill,
        "results_per_page": 10
    }
    response = requests.get(url, params=params)
    data = response.json()
    print(f"Jobs found for '{skill}': {data['count']}")

# Try different skills and compare
for skill in ["machine learning", "react", "cloud computing", "python"]:
    get_tech_jobs(skill)