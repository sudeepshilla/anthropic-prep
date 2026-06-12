from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Incident(BaseModel):
    application: str
    severity: str
    description: str

class AnalysisRequest(BaseModel):
    application: str
    error: str

@app.get("/")
def root():
    return {
        "message": "Hello Anthropic",
        "author": "Sudeep Kumar Shilla"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.post("/incident")
def create_incident(incident: Incident):

    severity_score = {
        "Low": 1,
        "Medium": 2,
        "High": 3,
        "Critical": 4
    }

    score = severity_score.get(incident.severity, 0)

    if score >= 4:
        priority = "P1"
    elif score >= 3:
        priority = "P2"
    else:
        priority = "P3"

    return {
        "status": "received",
        "application": incident.application,
        "severity": incident.severity,
        "priority": priority,
        "summary": f"Incident logged for {incident.application}"
    }

@app.post("/analyze")
def analyze_issue(request: AnalysisRequest):

    causes = []

    if "lag" in request.error.lower():
        causes.append("Slow consumer processing")
        causes.append("Partition imbalance")
        causes.append("Broker overload")

    elif "queue" in request.error.lower():
        causes.append("Queue manager issue")
        causes.append("Channel connectivity problem")

    else:
        causes.append("Further investigation required")

    return {
        "application": request.application,
        "possible_causes": causes
    }