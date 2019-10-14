from sqlalchemy import Column, Integer, String, DateTime
from database import Base


class Failure(Base):
    __tablename__ = 'failures'

    id = Column(Integer, primary_key=True)
    failure = Column(String(50))
    count = Column(String(120))
    status = Column(String(120))

    def __init__(self, failure=None, count=None, status=None):
        self.failure = failure
        self.count = count
        self.status = status

    def __repr__(self):
        return '<Failure %r>' % (self.failure)