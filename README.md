# Ground Reality
The job market, honestly. For CS students in India.
A full-stack dashboard that combines live economic data, real-time job market trends, and AI-generated analysis to help CS students understand how global events affect their career prospects.

## Features
- Live Indian economic indicators (GDP, inflation, unemployment)
- Real-time skill demand tracker across 8 tech skills in India
- Latest tech/economy news aggregated and filtered
- AI-generated career analysis specific to CS students in India

## Tech Stack
Python · Flask · JavaScript · HTML/CSS · REST APIs · Claude AI

## APIs Used
- News API — economic and tech news
- World Bank API — India economic indicators
- FRED API — US Fed rate
- Adzuna API — live job postings in India
- Anthropic API — AI analysis

## Setup
1. Clone the repo
2. Create a `.env` file in `/backend` with your API keys
3. Install dependencies: `pip install flask flask-cors requests python-dotenv`
4. Run: `py app.py`
5. Open `http://127.0.0.1:5000`
