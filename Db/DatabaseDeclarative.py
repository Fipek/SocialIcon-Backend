from sqlalchemy import Column,ForeignKey,Integer,String,DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Account(Base):
    __tablename__='ACCOUNT'
    ID = Column(Integer,primary_key=True)
    EMAIL = Column(String(50),unique=True)
    PASSWORD = Column(String(30))
    PHONE = Column(String(30))
    
class Profile(Base):
    __tablename__='PROFILE'
    ID = Column(Integer,primary_key=True,unique=True)
    FULLNAME = Column(String(100))
    USERNAME = Column(String(50),unique=True)
    PICTURE = Column(String(150))
    
class Offer(Base):
    __tablename__='OFFER'
    OFFER_ID = Column(Integer,primary_key=True)
    USER_ID = Column(Integer)
    URL = Column(String(150),unique=True)
    TITLE = Column(String(100))
    PLATFORM_ID = Column(Integer)
    COIN = Column(Integer) 
    DURATION = Column(Integer)
    COUNTER = Column(Integer)
    CREATE_DATE = Column(DateTime)
    LIKE_COUNT = Column(Integer)
    SHARE_COUNT = Column(Integer)
    AGREEMENT_COUNT = Column(Integer)
    VIEWING_COUNT = Column(Integer)
    
class OfferLikeYoutube(Base):
    __tablename__='OFFER_LIKE_YOUTUBE'
    OFFER_ID = Column(Integer,primary_key=True)
    USER_ID = Column(Integer,primary_key=True)
    CREATE_DATE = Column(DateTime)
    
class OfferViewingLog(Base):
    __tablename__='OFFER_VIEWING_LOG'
    ROW_ID = Column(Integer,primary_key=True)
    OFFER_ID = Column(Integer)
    USER_ID = Column(Integer)
    CREATE_DATE = Column(DateTime)
    
class OfferAgreementYoutube(Base):
    __tablename__='OFFER_AGREEMENT_YOUTUBE'
    OFFER_ID = Column(Integer,primary_key=True)
    USER_ID = Column(Integer,primary_key=True)
    CREATE_DATE = Column(DateTime)
    
class SessionStorage(Base):
    __tablename__='SESSION_STORAGE'
    USER_ID = Column(Integer,primary_key=True)
    TOKEN = Column(String(100),primary_key=True)
    IP_ADRESS = Column(String(25))
    USER_AGENT = Column(String(100))
    CREATE_DATE = Column(DateTime)
    
    
    
