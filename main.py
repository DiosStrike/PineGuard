from fastapi import FastAPI, HTTPException
import json
import os

app = FastAPI()
DATA_DIR = "data/processed"

@app.get("/analyze/{year}")
def get_analysis(year: str):
    file_path = os.path.join(DATA_DIR, f"stress_{year}.json")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Data not found")
    with open(file_path, "r") as f:
        return json.load(f)

@app.get("/stats/annual_outbreak_counts")
def get_annual_outbreak_counts():
    all_stats = []
    for year in range(1984, 2026):
        file_path = os.path.join(DATA_DIR, f"stress_{year}.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
                all_stats.append({"year": year, "outbreak_count": data["outbreak_count"]})
    return all_stats