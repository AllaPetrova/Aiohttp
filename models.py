from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import aiopg.sa

Base = declarative_base()


class Advertisement(Base):
    __tablename__ = 'advertisements'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(1000))
    created_at = Column(DateTime, default=datetime.utcnow)
    owner = Column(String(100), nullable=False)


engine = create_engine('sqlite:///ads.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


async def init_db(app):
    app['db'] = Session()


async def close_db(app):
    app['db'].close()
