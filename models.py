from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from database import Base


class IncidentDB(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    application = Column(String)
    severity = Column(String)
    description = Column(String)
    priority = Column(String)