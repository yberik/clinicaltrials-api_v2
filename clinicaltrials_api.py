from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI(title="ClinicalTrials.gov Proxy API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

BASE = "https://clinicaltrials.gov/api/v2/studies"
API_KEY = os.getenv("CLINICALTRIALS_API_KEY")

@app.get("/clinicaltrials")
def get_trials(term: str = Query(...), limit: int = Query(20, le=100)):
    headers = {"User-Agent": "pharma-bizdev-scout/1.0"}
    if API_KEY:
        headers["X-API-Key"] = API_KEY
    params = {
        "query.term": term,
        "pageSize": limit,
        "fields": "NCTId,BriefTitle,Condition,Phase,OverallStatus,SponsorName,LocationCountry"
    }
    r = requests.get(BASE, headers=headers, params=params)
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)
    data = r.json()
    return {"count": len(data.get("studies", [])), "term": term, "results": data.get("studies", [])}
