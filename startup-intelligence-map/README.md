# Startup Ecosystem Intelligence Map

A hackathon-ready dashboard that analyzes GitHub activity, job listings, and tech news to identify which startup sectors are growing fastest.

## Quick Start

```bash
# 1. Install dependencies
pip install flask requests

# 2. Run the app
cd backend
python app.py

# 3. Open browser
# Landing page: http://localhost:5000
# Dashboard:    http://localhost:5000/dashboard
```

## Project Structure

```
startup-intelligence-map/
├── backend/
│   ├── app.py              # Flask app + API routes
│   ├── data_processing.py  # Data aggregation + trend scoring
│   └── sector_classifier.py # Keyword-based sector classification
├── templates/
│   ├── index.html          # Landing page
│   └── dashboard.html      # Analytics dashboard
└── requirements.txt
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/trends` | Trend scores per sector (0-100) |
| `GET /api/news` | Latest tech news by sector |
| `GET /api/jobs` | Job postings by sector |
| `GET /api/startups` | Startups categorized by sector |
| `GET /api/prediction` | AI growth predictions |
| `GET /api/map-data` | City startup activity data |
| `GET /api/historical` | 7-month trend history |

## Trend Score Formula

```
trend_score = (github_repos × 0.4) + (job_postings × 0.3) + (news_mentions × 0.3)
```

Scores are normalized 0-100 with sector-specific momentum multipliers.

## Sectors Tracked

- 🤖 AI / Machine Learning
- 🛠 DevTools  
- 💳 Fintech
- 🔐 Cybersecurity
- 🏥 Health Tech
- 🤖 Robotics
- 🌱 Climate Tech

## Connecting Real APIs

In `data_processing.py`, replace mock data with real API calls:

### GitHub API
```python
import requests
headers = {'Authorization': 'token YOUR_GITHUB_TOKEN'}
r = requests.get('https://api.github.com/search/repositories?q=AI&sort=stars', headers=headers)
```

### NewsAPI
```python
r = requests.get(f'https://newsapi.org/v2/everything?q=startup+AI&apiKey=YOUR_KEY')
```

### Adzuna Jobs API
```python
r = requests.get('https://api.adzuna.com/v1/api/jobs/us/search/1?app_id=ID&app_key=KEY&what=AI+engineer')
```

## Tech Stack

- **Backend**: Python + Flask
- **Frontend**: HTML5, CSS3, Vanilla JS
- **Charts**: Chart.js 4.4
- **Maps**: Leaflet.js 1.9
- **Data**: Mock data (hackathon-ready, swap for live APIs)
