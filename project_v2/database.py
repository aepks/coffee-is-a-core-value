from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, DateTime, Float, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func

engine = create_engine('postgresql+psycopg2://aepks:aepks@localhost/aepks_accounts', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column('id', Integer, primary_key=True)
    rfid_key = Column('rfid_key', Integer, unique=True)
    username = Column('username', String)
    email = Column('email', String)
    disabled = Column('disabled', Boolean)

class Role(Base):
    __tablename__ = 'role'
    id = Column('id', Integer, primary_key=True)
    rfid_key = Column('rfid_key', Integer, unique=True)
    role = Column('role', String)

class Transaction(Base):
    # Reference Stack Overflow 13370317
    __tablename__ = 'transactions'
    rfid_key = Column('rfid_key', Integer, primary_key = True)
    transaction_id = Column('transaction_id', Integer, unique=True, primary_key=True)
    timestamp = Column('timestamp', DateTime(timezone=True), server_default=func.now())
    price = Column('price', Float(precision=2))

class Item(Base):
    __tablename__ = 'item'
    id=Column('id',Integer,primary_key=True)
    name=Column('name',String,unique=True)
    price=Column('price',Float(precision=2))

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

# user = User()
# user.rfid_key = 1234
# user.username = "jschmitz2"
# user.email = "jschmitz2@hawk.iit.edu"
# user.disabled = False

# session.add(user)



session.close()
