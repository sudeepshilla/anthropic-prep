from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey
)
from datetime import datetime
from database import Base
from sqlalchemy.orm import relationship

class IncidentDB(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)

    application = Column(String)
    severity = Column(String)
    description = Column(String)

    priority = Column(String)

    analysis_records = relationship(
        "IncidentAnalysis",
        back_populates="incident"
    )

class IncidentAnalysis(Base):
    __tablename__ = "incident_analysis"

    id = Column(Integer, primary_key=True, index=True)

    incident_id = Column(
        Integer,
        ForeignKey("incidents.id")
    )

    analysis = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    incident = relationship(
        "IncidentDB",
        back_populates="analysis_records"
    )