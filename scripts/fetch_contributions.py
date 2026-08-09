#!/usr/bin/env python3
"""
Fetch GitHub contribution calendar from public HTML page.
No auth required. Parses day cells and writes data/contributions.json.
"""
import json
import sys
from datetime import datetime, date, timedelta
import requests
from bs4 import BeautifulSoup

USERNAME = "arghyajit18"
URL = f"https://github.com/users/{USERNAME}/contributions"

def fetch_contributions():
    headers = {"User-Agent": "Mozilla/5.0 (compatible; GitHubProfileArt/1.0)"}
    resp = requests.get(URL, headers=headers, timeout=30)
    resp.raise_for_status()
    
    soup = BeautifulSoup(resp.text, "html.parser")
    
    # Find the contribution calendar
    days = []
    for rect in soup.select("svg g rect[data-date]"):
        data_date = rect.get("data-date")
        data_count = int(rect.get("data-count", 0))
        data_level = int(rect.get("data-level", 0))
        days.append({
            "date": data_date,
            "count": data_count,
            "level": data_level,
        })
    
    if not days:
        # Fallback: try the newer calendar format
        for td in soup.select("td[data-date]"):
            data_date = td.get("data-date")
            data_count = int(td.get("data-count", 0))
            data_level = int(td.get("data-level", 0))
            days.append({
                "date": data_date,
                "count": data_count,
                "level": data_level,
            })
    
    # Sort by date
    days.sort(key=lambda d: d["date"])
    
    # Calculate derived stats
    today = date.today()
    one_year_ago = today - timedelta(days=365)
    
    # Filter last year
    recent_days = [d for d in days if d["date"] >= one_year_ago.isoformat()]
    
    # Current streak
    current_streak = 0
    for d in reversed(recent_days):
        if d["count"] > 0:
            current_streak += 1
        else:
            break
    
    # Longest streak
    longest_streak = 0
    streak = 0
    for d in recent_days:
        if d["count"] > 0:
            streak += 1
            longest_streak = max(longest_streak, streak)
        else:
            streak = 0
    
    # Best day
    best_day = max(recent_days, key=lambda d: d["count"]) if recent_days else {"date": "", "count": 0}
    
    # Monthly totals
    monthly = {}
    for d in recent_days:
        month = d["date"][:7]  # YYYY-MM
        monthly[month] = monthly.get(month, 0) + d["count"]
    
    total_contributions = sum(d["count"] for d in recent_days)
    
    data = {
        "username": USERNAME,
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "days": days,
        "stats": {
            "total_last_year": total_contributions,
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "best_day": best_day,
            "monthly_totals": monthly,
        }
    }
    
    with open("data/contributions.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Fetched {len(days)} days, {total_contributions} contributions in last year")
    print(f"Current streak: {current_streak}, Longest: {longest_streak}")

if __name__ == "__main__":
    fetch_contributions()