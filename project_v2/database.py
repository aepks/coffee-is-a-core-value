from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, DateTime, Float, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
import random

engine = create_engine('postgresql+psycopg2://aepks:aepks@localhost/aepks_accounts', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    rfid_key = Column(Integer, unique=True)
    username = Column(String)
    email = Column(String)
    disabled = Column(Boolean)

    # Relatoinship structures
    transactions = relationship('Transaction', back_populates='user')
    role = relationship("Role", uselist=False, back_populates='user')

class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    role = Column(String)
    user = relationship("User", back_populates='role', uselist=False)

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    amount = Column(Float(precision=2))
    # Relationship to User
    user = relationship('User', back_populates='transactions')

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer,primary_key=True)
    name = Column(String,unique=True)
    price = Column(Float(precision=2))

def return_user(rfid_key):
    for user in session.query(User).filter_by(rfid_key=rfid_key):
        return user
    new_user = User(rfid_key=rfid_key, username=None,email=None,disabled=0)

    # For testing purposes: Add random transactions to account.

    for _ in range(30):
        new_user.transactions.append(random.randrange(-5,5))
    session.add(new_user)
    session.commit()
    return new_user

def user_balance(user):
    return sum([transaction for transaction in session.query(User.transactions)])




Base.metadata.create_all(bind=engine)
