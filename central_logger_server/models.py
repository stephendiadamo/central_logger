from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('sqlite:///central_logger.db', echo=False)
Base = declarative_base()


class Error(Base):
    __tablename__ = 'error'

    id = Column(Integer, primary_key=True)
    error_type = Column(String(100))
    description = Column(String(200), nullable=True)
    occurred_at = Column(String(50))

    def __init__(self, error_type, description=None, occurred_at=None):
        self.error_type = error_type
        self.description = description
        if occurred_at is None:
            occurred_at = str(datetime.now())
        self.occurred_at = occurred_at

    @property
    def serialize(self):
        return {
            'id': self.id,
            'error_type': self.error_type,
            'description': self.description,
            'occurred_at': self.occurred_at
        }


Base.metadata.create_all(engine)
