from fastapi import FastAPI
from pydantic import BaseModel
from database import engine
from database import SessionLocal
from database import Base
from models import IncidentDB

import models

Base.metadata.create_all(bind=engine)

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

    db = SessionLocal()

    db_incident = IncidentDB(
        application=incident.application,
        severity=incident.severity,
        description=incident.description,
        priority=priority
    )

    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)

    db.close()

    return {
        "id": db_incident.id,
        "application": db_incident.application,
        "severity": db_incident.severity,
        "description": db_incident.description,
        "priority": db_incident.priority
    }

@app.get("/incidents")
def get_incidents():

    db = SessionLocal()

    incidents = db.query(IncidentDB).all()

    result = []

    for incident in incidents:
        result.append({
            "id": incident.id,
            "application": incident.application,
            "severity": incident.severity,
            "description": incident.description,
            "priority": incident.priority
        })

    db.close()

    return result

@app.get("/incident/{incident_id}")
def get_incident(incident_id: int):

    db = SessionLocal()

    incident = db.query(IncidentDB).filter(
        IncidentDB.id == incident_id
    ).first()

    db.close()

    if incident is None:
        return {"error": "Incident not found"}

    return {
        "id": incident.id,
        "application": incident.application,
        "severity": incident.severity,
        "description": incident.description,
        "priority": incident.priority
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