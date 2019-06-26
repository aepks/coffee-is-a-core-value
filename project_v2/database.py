from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime
from mail import SendMessage
import random

engine = create_engine('postgresql+psycopg2://aepks:aepks@localhost/aepks')
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
    fingerprint = Column(Integer, unique=True)
    # Relatoinship structures
    transactions = relationship('Transaction', back_populates='user')
    role = relationship("Role", uselist=False, back_populates='user')

    def balance(self):
        return sum([transaction.amount for transaction in self.transactions])

    def price(self, item):
        return self.role.price(item)

    def active_test(self):
        # Takes no argument.
        # Returns false if a user has not paid in full in the past two weeks.
        # Returns true otherwise.

        balance = 0
        last_current = None
        for transaction in self.transactions:  # chronological order
            balance += transaction.amount
            if balance == 0:
                last_current = transaction.timestamp

        now = datetime.now()
        delta = now - last_current
        if delta.days > 14:
            return False
        else:
            return True



    def history(self):
        history = []
        for transaction in self.transactions:
            if transaction.amount < 0:
                type = 'Purchase'
            else:
                type = 'Credit'

            history.append(
                '<li>'
                f'{transaction.timestamp.month}/'
                f'{transaction.timestamp.day}, '
                f'{transaction.timestamp.hour}:'
                f'{transaction.timestamp.minute}, '
                f'{type} for '
                f'{abs(transaction.amount)}'
                '</li>')

        history.reverse()
        d = datetime.today()
        subject = f"""Your Coffee Machine History as of {d.month} - {d.day}"""
        msgPlain = "\n  - ".join(history)

        msgHTML = ("<h2> See your transaction history listed below.</h2>")
        msgHTML += "<ul>"
        msgHTML = msgHTML + "\n".join(history)
        msgHTML += "</ul>"
        msgHTML += (
            "<p><em>If you have any questions or concerns,"
            " reply to this email.</em></p>"
        )

        SendMessage(self.email, subject, msgHTML, msgPlain)

    def purchase(self, item):
        price = self.price(item)
        print(price)
        self.transactions.append(Transaction(amount=(price*-1)))

        subject = "Thank you for your coffee purchase!"
        msgPlain = "Thanks for buying a coffee!"
        msgHTML = "<h1>Thanks for buying a coffee!</h1>"
        msgHTML += (
            "<p>Hey, thanks for buying a coffee! Your current balance is "
            f"{self.balance()}<br><br> <em>If you're recieving"
            f"this message, but didn't buy a coffee, reply to this "
            f"email <strong>as soon as possible</strong>, "
            f"because you were certainly charged for one.</em></p>"
        )

        SendMessage(self.email, subject, msgHTML, msgPlain)


class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String)
    permissions = Column(Boolean)
    user = relationship('User', back_populates='role')
    items = relationship('Item')

    def price(self, purchase):
        for item in self.items:
            print(item.name, purchase)
            if item.name == purchase:
                return item.price
        else:
            return False  # set this up to failsafe

    def add_item(self, item, price):
        self.items.append(Item(name=item, price=price))

    def update_item(self, item, price):

        if item == "*":
            for item in self.prices:
                item.price = price
        else:
            for item in self.prices:
                if item.name == item:
                    item.price = price


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(Integer, ForeignKey('role.id'))
    price = Column(Float(precision=2))


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    amount = Column(Float(precision=2))
    user = relationship('User', back_populates='transactions')

###############################################################


def add_item(item, price):
    for role in session.query(Role):
        role.add_item(item, price)


def return_user(rfid_key):

    for user in session.query(User).filter_by(rfid_key=rfid_key):
        return user
    # else:
    new_user = User(rfid_key=rfid_key, username=None, email=None, disabled=0)
    for _ in range(30):
        new_user.transactions.append(random.randrange(-5, 5))
    session.add(new_user)
    session.commit()
    return new_user


def flag_delinquent():  # figure out a better way to integrate this
    for user in session.query(User):
        user.active = user.active_test()


Base.metadata.create_all(engine)


# test_user = User(rfid_key=113815,disabled=False)
# test_user.username="jschmitz2"
# test_user.email="jschmtiz2@hawk.iit.edu"
# test_user.disabled=True
# test_user.transactions.append(Transaction(amount=0.5))

# session.add(test_user)


user = return_user(113815)
user.purchase("coffee")
# user.role = Role(name="user",permissions=0)
# user.role.add_item("coffee", .5)
# for x in range(1000):
#     user.purchase("coffee")

# user.email="jschmitz2@hawk.iit.edu"
# user.history()

session.commit()
