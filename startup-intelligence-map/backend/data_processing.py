import json
import os
import random
from datetime import datetime, timedelta
from sector_classifier import SectorClassifier

classifier = SectorClassifier()

MOCK_GITHUB_DATA = {
    "AI": [
        {"name": "ollama", "stars": 89000, "description": "Get up and running with LLMs locally", "topics": ["ai", "llm", "machine-learning"]},
        {"name": "open-interpreter", "stars": 54000, "description": "A natural language interface for computers", "topics": ["ai", "llm", "automation"]},
        {"name": "localai", "stars": 22000, "description": "Free, Open Source OpenAI alternative", "topics": ["ai", "llm", "openai"]},
        {"name": "litellm", "stars": 15000, "description": "Call all LLM APIs using the OpenAI format", "topics": ["ai", "llm", "api"]},
        {"name": "phidata", "stars": 11000, "description": "Build AI Assistants with memory, knowledge and tools", "topics": ["ai", "agents", "llm"]},
    ],
    "Fintech": [
        {"name": "freqtrade", "stars": 28000, "description": "Free, open source crypto trading bot", "topics": ["fintech", "crypto", "trading"]},
        {"name": "moneydance", "stars": 4200, "description": "Personal finance manager", "topics": ["fintech", "banking"]},
        {"name": "rotki", "stars": 2800, "description": "Accounting, asset management and tax reporting for crypto", "topics": ["fintech", "crypto", "defi"]},
    ],
    "Climate Tech": [
        {"name": "electricitymaps", "stars": 3800, "description": "Real-time electricity CO2 emissions map", "topics": ["climate", "energy", "carbon"]},
        {"name": "openenergymonitor", "stars": 2100, "description": "Open source energy monitoring platform", "topics": ["climate", "energy", "renewable"]},
        {"name": "carbonplan", "stars": 890, "description": "Climate science and policy tools", "topics": ["climate", "carbon"]},
    ],
    "Robotics": [
        {"name": "ros2", "stars": 8900, "description": "Robot Operating System 2", "topics": ["robotics", "ros", "autonomous"]},
        {"name": "drake", "stars": 3200, "description": "Model-based design and verification for robotics", "topics": ["robotics", "automation"]},
        {"name": "moveit2", "stars": 1900, "description": "Motion planning framework for robotics", "topics": ["robotics", "automation"]},
    ],
    "Cybersecurity": [
        {"name": "metasploit-framework", "stars": 33000, "description": "World's most used penetration testing framework", "topics": ["cybersecurity", "pentesting"]},
        {"name": "nuclei", "stars": 20000, "description": "Fast and customizable vulnerability scanner", "topics": ["cybersecurity", "vulnerability"]},
        {"name": "wazuh", "stars": 10000, "description": "Open source security platform", "topics": ["cybersecurity", "siem", "xdr"]},
    ],
    "Health Tech": [
        {"name": "openmrs", "stars": 4100, "description": "Open source medical records system", "topics": ["health", "ehr", "medtech"]},
        {"name": "medplum", "stars": 1800, "description": "Healthcare developer platform", "topics": ["health", "fhir", "medtech"]},
        {"name": "healthchecks", "stars": 7200, "description": "Cron job monitoring service", "topics": ["devtools", "monitoring"]},
    ],
    "DevTools": [
        {"name": "gitbutler", "stars": 12000, "description": "A Git client for simultaneous branches", "topics": ["devtools", "git", "developer"]},
        {"name": "zed", "stars": 49000, "description": "High-performance, multiplayer code editor", "topics": ["devtools", "ide", "editor"]},
        {"name": "mise-en-place", "stars": 9800, "description": "Dev tools, env vars, task runner", "topics": ["devtools", "cli", "developer"]},
        {"name": "dagger", "stars": 11000, "description": "Programmable CI/CD engine", "topics": ["devtools", "cicd", "cloud"]},
    ]
}

MOCK_JOB_DATA = {
    "AI": [
        {"title": "Senior ML Engineer", "company": "OpenAI", "location": "San Francisco", "skills": ["python", "pytorch", "llm"], "salary": "$180k-$280k"},
        {"title": "AI Research Scientist", "company": "Anthropic", "location": "San Francisco", "skills": ["ml", "deep learning", "transformers"], "salary": "$200k-$350k"},
        {"title": "LLM Product Engineer", "company": "Cohere", "location": "Toronto", "skills": ["llm", "python", "api"], "salary": "$140k-$200k"},
        {"title": "ML Platform Engineer", "company": "Hugging Face", "location": "Remote", "skills": ["mlops", "kubernetes", "pytorch"], "salary": "$150k-$220k"},
        {"title": "AI Engineer", "company": "Mistral AI", "location": "Paris", "skills": ["ai", "python", "ml"], "salary": "€120k-€180k"},
    ],
    "Fintech": [
        {"title": "Blockchain Developer", "company": "Coinbase", "location": "San Francisco", "skills": ["solidity", "web3", "defi"], "salary": "$160k-$240k"},
        {"title": "Payments Engineer", "company": "Stripe", "location": "Dublin", "skills": ["payments", "api", "python"], "salary": "€100k-€160k"},
        {"title": "Quant Developer", "company": "Revolut", "location": "London", "skills": ["fintech", "trading", "python"], "salary": "£90k-£140k"},
    ],
    "Climate Tech": [
        {"title": "Climate Data Scientist", "company": "Tomorrow.io", "location": "Boston", "skills": ["climate", "python", "ml"], "salary": "$130k-$180k"},
        {"title": "Energy Systems Engineer", "company": "Tesla Energy", "location": "Austin", "skills": ["ev", "battery", "energy"], "salary": "$140k-$200k"},
        {"title": "Carbon Analytics Lead", "company": "Watershed", "location": "San Francisco", "skills": ["climate", "data", "carbon"], "salary": "$150k-$210k"},
    ],
    "Robotics": [
        {"title": "Robotics Software Engineer", "company": "Boston Dynamics", "location": "Waltham", "skills": ["ros", "c++", "robotics"], "salary": "$160k-$220k"},
        {"title": "Autonomous Systems Engineer", "company": "Figure AI", "location": "San Jose", "skills": ["robotics", "ml", "hardware"], "salary": "$180k-$250k"},
        {"title": "Computer Vision Engineer", "company": "Agility Robotics", "location": "Corvallis", "skills": ["vision", "robotics", "python"], "salary": "$140k-$190k"},
    ],
    "Cybersecurity": [
        {"title": "Security Engineer", "company": "CrowdStrike", "location": "Austin", "skills": ["cybersecurity", "xdr", "cloud"], "salary": "$150k-$220k"},
        {"title": "Threat Intel Analyst", "company": "Palo Alto Networks", "location": "Santa Clara", "skills": ["soc", "threat", "siem"], "salary": "$130k-$180k"},
        {"title": "Zero Trust Architect", "company": "Zscaler", "location": "San Jose", "skills": ["zero-trust", "iam", "security"], "salary": "$160k-$230k"},
    ],
    "Health Tech": [
        {"title": "Bioinformatics Engineer", "company": "Illumina", "location": "San Diego", "skills": ["genomics", "python", "biotech"], "salary": "$140k-$200k"},
        {"title": "Digital Health PM", "company": "Tempus AI", "location": "Chicago", "skills": ["health", "ai", "clinical"], "salary": "$130k-$180k"},
        {"title": "Medical AI Researcher", "company": "PathAI", "location": "Boston", "skills": ["health", "ml", "radiology"], "salary": "$150k-$210k"},
    ],
    "DevTools": [
        {"title": "Developer Advocate", "company": "Vercel", "location": "Remote", "skills": ["devtools", "javascript", "cloud"], "salary": "$130k-$180k"},
        {"title": "Platform Engineer", "company": "Datadog", "location": "New York", "skills": ["observability", "devops", "cloud"], "salary": "$170k-$240k"},
        {"title": "CLI Engineer", "company": "GitHub", "location": "Remote", "skills": ["devtools", "go", "cli"], "salary": "$160k-$220k"},
        {"title": "Infrastructure Engineer", "company": "Railway", "location": "Remote", "skills": ["devops", "kubernetes", "cloud"], "salary": "$140k-$200k"},
    ]
}

MOCK_NEWS_DATA = [
    {"title": "Anthropic raises $4B Series E to accelerate Claude development", "sector": "AI", "type": "funding", "date": "2025-01-15", "source": "TechCrunch"},
    {"title": "OpenAI launches o3 model with record reasoning capabilities", "sector": "AI", "type": "product", "date": "2025-01-12", "source": "The Verge"},
    {"title": "Figure AI's humanoid robot begins commercial deployments", "sector": "Robotics", "type": "milestone", "date": "2025-01-10", "source": "Wired"},
    {"title": "Stripe acquires Bridge for $1.1B in stablecoin payments play", "sector": "Fintech", "type": "acquisition", "date": "2025-01-08", "source": "Bloomberg"},
    {"title": "CrowdStrike expands AI-powered threat detection suite", "sector": "Cybersecurity", "type": "product", "date": "2025-01-07", "source": "ZDNet"},
    {"title": "Watershed raises $100M to help Fortune 500 reach net zero", "sector": "Climate Tech", "type": "funding", "date": "2025-01-06", "source": "Reuters"},
    {"title": "Vercel introduces AI-native deployment pipeline with Edge AI", "sector": "DevTools", "type": "product", "date": "2025-01-05", "source": "Hacker News"},
    {"title": "Tempus AI goes public at $6B valuation on AI diagnostics boom", "sector": "Health Tech", "type": "ipo", "date": "2025-01-04", "source": "WSJ"},
    {"title": "Google DeepMind's Gemini 2.0 Flash outperforms on coding benchmarks", "sector": "AI", "type": "research", "date": "2025-01-03", "source": "Nature"},
    {"title": "Agility Robotics deploys 500 Digit robots at Amazon warehouses", "sector": "Robotics", "type": "deployment", "date": "2025-01-02", "source": "Forbes"},
    {"title": "Coinbase launches international derivatives exchange", "sector": "Fintech", "type": "product", "date": "2024-12-30", "source": "CoinDesk"},
    {"title": "Zed editor hits 1M downloads, challenges VS Code dominance", "sector": "DevTools", "type": "milestone", "date": "2024-12-28", "source": "Hacker News"},
    {"title": "PathAI raises $165M Series D for AI-powered cancer diagnostics", "sector": "Health Tech", "type": "funding", "date": "2024-12-27", "source": "STAT News"},
    {"title": "Tesla Energy's Megapack breaks record with 10GWh deployment", "sector": "Climate Tech", "type": "milestone", "date": "2024-12-25", "source": "Electrek"},
    {"title": "Zscaler reports 40% YoY growth as zero trust adoption accelerates", "sector": "Cybersecurity", "type": "earnings", "date": "2024-12-24", "source": "Reuters"},
]

MOCK_MAP_DATA = [
    {"city": "San Francisco", "lat": 37.7749, "lng": -122.4194, "startups": 847, "dominant_sector": "AI", "growth": 34},
    {"city": "New York", "lat": 40.7128, "lng": -74.0060, "startups": 623, "dominant_sector": "Fintech", "growth": 22},
    {"city": "London", "lat": 51.5074, "lng": -0.1278, "startups": 512, "dominant_sector": "Fintech", "growth": 19},
    {"city": "Berlin", "lat": 52.5200, "lng": 13.4050, "startups": 298, "dominant_sector": "Climate Tech", "growth": 31},
    {"city": "Bangalore", "lat": 12.9716, "lng": 77.5946, "startups": 441, "dominant_sector": "DevTools", "growth": 28},
    {"city": "Singapore", "lat": 1.3521, "lng": 103.8198, "startups": 289, "dominant_sector": "Fintech", "growth": 24},
    {"city": "Austin", "lat": 30.2672, "lng": -97.7431, "startups": 187, "dominant_sector": "AI", "growth": 41},
    {"city": "Boston", "lat": 42.3601, "lng": -71.0589, "startups": 312, "dominant_sector": "Health Tech", "growth": 18},
    {"city": "Tel Aviv", "lat": 32.0853, "lng": 34.7818, "startups": 267, "dominant_sector": "Cybersecurity", "growth": 29},
    {"city": "Toronto", "lat": 43.6532, "lng": -79.3832, "startups": 198, "dominant_sector": "AI", "growth": 35},
    {"city": "Paris", "lat": 48.8566, "lng": 2.3522, "startups": 221, "dominant_sector": "AI", "growth": 27},
    {"city": "Tokyo", "lat": 35.6762, "lng": 139.6503, "startups": 334, "dominant_sector": "Robotics", "growth": 16},
    {"city": "Stockholm", "lat": 59.3293, "lng": 18.0686, "startups": 156, "dominant_sector": "Climate Tech", "growth": 33},
    {"city": "Sydney", "lat": -33.8688, "lng": 151.2093, "startups": 143, "dominant_sector": "Health Tech", "growth": 21},
]

HISTORICAL_DATA = {
    "labels": ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan"],
    "datasets": {
        "AI": [62, 65, 71, 76, 81, 84, 87],
        "Fintech": [48, 49, 51, 52, 53, 54, 54],
        "Climate Tech": [22, 24, 25, 27, 28, 28, 29],
        "Robotics": [26, 27, 28, 29, 31, 31, 32],
        "Cybersecurity": [44, 45, 46, 47, 48, 49, 51],
        "Health Tech": [35, 36, 37, 38, 39, 40, 42],
        "DevTools": [56, 57, 59, 61, 62, 63, 65],
    }
}

class DataProcessor:
    def __init__(self):
        self.classifier = SectorClassifier()

    def get_github_data(self):
        return MOCK_GITHUB_DATA

    def get_news_data(self):
        return MOCK_NEWS_DATA

    def get_job_data(self):
        return MOCK_JOB_DATA

    def get_startup_data(self):
        startups = {}
        for sector, repos in MOCK_GITHUB_DATA.items():
            startups[sector] = [
                {"name": r["name"], "description": r["description"], "stars": r["stars"]}
                for r in repos
            ]
        return startups

    def get_map_data(self):
        return MOCK_MAP_DATA

    def get_historical_data(self):
        return HISTORICAL_DATA

    def get_all_data(self):
        return {
            "github": self.get_github_data(),
            "news": self.get_news_data(),
            "jobs": self.get_job_data(),
        }

    def calculate_trend_scores(self, data):
        sectors = ["AI", "Fintech", "Climate Tech", "Robotics", "Cybersecurity", "Health Tech", "DevTools"]
        scores = {}

        github_counts = {s: len(data["github"].get(s, [])) for s in sectors}
        job_counts = {s: len(data["jobs"].get(s, [])) for s in sectors}
        news_counts = {s: sum(1 for n in data["news"] if n["sector"] == s) for s in sectors}

        max_github = max(github_counts.values(), default=1)
        max_jobs = max(job_counts.values(), default=1)
        max_news = max(news_counts.values(), default=1)

        for sector in sectors:
            g_norm = (github_counts[sector] / max_github) * 100
            j_norm = (job_counts[sector] / max_jobs) * 100
            n_norm = (news_counts[sector] / max_news) * 100
            raw = (g_norm * 0.4) + (j_norm * 0.3) + (n_norm * 0.3)
            # Apply sector-specific multipliers based on current momentum
            multipliers = {
                "AI": 1.35, "DevTools": 1.15, "Cybersecurity": 1.05,
                "Fintech": 0.92, "Health Tech": 0.88,
                "Robotics": 0.82, "Climate Tech": 0.75
            }
            scores[sector] = round(min(99, raw * multipliers.get(sector, 1.0)))

        return scores

    def generate_prediction(self, data):
        trends = self.calculate_trend_scores(data)
        historical = HISTORICAL_DATA["datasets"]

        predictions = []
        for sector, current_score in trends.items():
            hist = historical.get(sector, [current_score])
            if len(hist) >= 2:
                recent_growth = hist[-1] - hist[-3] if len(hist) >= 3 else hist[-1] - hist[-2]
                momentum = recent_growth / max(hist[-3] if len(hist) >= 3 else hist[-2], 1) * 100
            else:
                momentum = 5.0
            predictions.append({
                "sector": sector,
                "current_score": current_score,
                "momentum": round(momentum, 1),
                "prediction_6m": round(momentum * 1.2, 1)
            })

        predictions.sort(key=lambda x: x["momentum"], reverse=True)
        top = predictions[0]
        return {
            "top_sector": top["sector"],
            "growth_prediction": top["prediction_6m"],
            "momentum": top["momentum"],
            "message": f"{top['sector']} is predicted to grow {top['prediction_6m']}% in the next 6 months based on current momentum.",
            "all_predictions": predictions
        }
