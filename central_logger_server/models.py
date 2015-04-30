from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('sqlite:///central_logger.db', echo=False)
Base = declarative_base()


class Log(Base):
    __tablename__ = 'log'

    id = Column(Integer, primary_key=True)
    log_type = Column(String(100))
    event_type = Column(String(100))
    application = Column(String(100))
    occurred_at = Column(String(50))
    description = Column(String(500), nullable=True)
    log_message = Column(String(800), nullable=True)

    def __init__(self, log_type, event_type, application, occurred_at=None, description=None, log_message=None):
        if occurred_at is None:
            occurred_at = str(datetime.now())

        self.log_type = log_type
        self.event_type = event_type
        self.application = application
        self.occurred_at = occurred_at
        self.description = description
        self.log_message = log_message

    @property
    def serialize(self):
        return {
            'id': self.id,
            'log_type': self.log_type,
            'event_type': self.event_type,
            'application': self.application,
            'occurred_at': self.occurred_at,
            'description': self.description,
            'log_message': self.log_message
        }


Base.metadata.create_all(engine)
