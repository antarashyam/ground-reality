import requests
import os
from dotenv import load_dotenv

load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_API_KEY = os.getenv("ADZUNA_API_KEY")

skills = [
    "machine learning",
    "react",
    "cloud computing",
    "python",
    "data science",
    "cybersecurity",
    "devops",
    "artificial intelligence"
]

def get_job_count(skill):
    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_API_KEY,
        "what": skill,
        "results_per_page": 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get("count", 0)

def get_all_skill_counts():
    results = {}
    for skill in skills:
        count = get_job_count(skill)
        results[skill] = count
        print(f"{skill}: {count} jobs")
    return results

get_all_skill_counts()