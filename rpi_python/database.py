from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, desc
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime
from mail import SendMessage
from gpio_interface import display
import random

# testing purposes

engine = create_engine('postgresql+psycopg2://aepks:aepks@localhost/aepks')
# engine = create_engine('sqlite://')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    """User Class for the Coffee Machine Account System

    ...
    Attributes
    ----------
    __tablename__ : str
        sql table name for sqlalchemy
    id: int
        primary table key. Autoincremented.
    username: str
        user's hawkcard username (jschmitz2, etc)
    email: str
        user's email.
    disabled: boolean
        boolean to determine whether user account should be locked or not.
    fingerprint: int
        fingerprints are slotted into integer positions by the r305
    transactions: [Transaction] (one to many)
        relationship to transactions, can be accessed as a list
    role: Role (one to one)
        relationship to roles, object is returned
    messages: [Message] (one to many)
        all email messages sent to user are stored, can be accessed as a list
    rfid_key: [RFID_key] (one to many)
        list of user's RFID keys - possible that if somebody gets a new card,
        they'd have a new RFID key and want to keep the same account.

    Methods
    -------
    last_transaction()
        Returns datetime. Last transaction time.

    last_message(type)
        Returns datetime. Takes in a string referring to message type.
        Returns the last time a particular type of message was sent
        to the user.

    balance()
        Returns float. Returns a user's current balance.

    price(item)
        Returns float. Returns an item's price for a user.

    active_test()
        Returns boolean. Returns false if a user has not paid in full within
        the last two weeks.

    invoice()
        Returns none. Sends the user an email with their current balance,
        as well as their transation history for the last two weeks.

    full_history()
        Returns none. Sends the user an email with their complete history.

    purchase(item)
        Returns none. Adds a transaction to the user's transactions. Sends
        the user an email thanking them for their transaction.


    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    disabled = Column(Boolean)
    fingerprint = Column(Integer, unique=True)
    # Relatoinship structures
    transactions = relationship('Transaction', back_populates='user')
    role = relationship("Role", uselist=False, back_populates='user')
    messages = relationship('Message', back_populates='user')
    rfid_key = relationship('RFID_key', back_populates='user')

    def last_transaction(self):
        time = None
        for transaction in self.transactions:
            time = transaction.timestamp()
        if time is None:
            return datetime.now()
        else:
            return time

    def last_message(self, type):
        time = None
        for message in self.messages:
            if message.type == type:
                time = message.timestamp  # assuming time always goes up
        if time is None:
            time = self.last_transaction()
        return time

    def balance(self):
        return sum([transaction.amount for transaction in self.transactions])

    def add_balance(self, amount):
        self.transactions.append(Transaction(amount=amount))

        subject = "Balance added to your AEPKS Coffee Account"
        msgPlain = f"{amount} has been added to your AEPKS coffee account!"
        msgHTML = f"<h1>${amount} has been added to your account!</h1>"
        msgHTML += (
            f"<p>${amount} has been added to your account! Your balance is "
            f"{self.balance()}<br><br> <em>If you're recieving"
            f"this message, but didn't put money in, reply to this "
            f"email <strong>as soon as possible</strong>."
        )

        SendMessage(self.email, subject, msgHTML, msgPlain)
        self.messages.append(Message(
            type="purchase",
            subject=subject,
            msgHTML=msgHTML,
            msgPlain=msgPlain)
        )


    def price(self, item):  # TODO: MAKE THIS METHOD NOT EXIST
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

    def invoice(self):
        last_invoice = self.last_message("invoice")
        if (datetime.now()-last_invoice).days > 14:
            history = []
            for transaction in self.transactions:
                if (datetime.now() - transaction.timestamp).days < 14:
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

            subject = f"""Your Coffee Machine Invoice as of {d.month} - {d.day}"""
            msgPlain = "\n  - ".join(history)
            msgHTML = (f"<h1> Your current balance is {self.balance()}.</h1>")
            msgHTML += ("<h2> See your transaction history listed below for the past two weeks.</h2>")
            msgHTML += "<ul>"
            msgHTML = msgHTML + "\n".join(history)
            msgHTML += "</ul>"
            msgHTML += (
                "<p><em>If you have any questions or concerns,"
                " reply to this email.</em></p>"
            )

            SendMessage(self.email, subject, msgHTML, msgPlain)
            self.messages.append(Message(
                type="invoice",
                subject=subject,
                msgHTML=msgHTML,
                msgPlain=msgPlain)
            )

    def full_history(self, email=True):
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

        if email:
            SendMessage(self.email, subject, msgHTML, msgPlain)
            self.messages.append(Message(
                type="full_history",
                subject=subject,
                msgHTML=msgHTML,
                msgPlain=msgPlain)
            )

        return history

    def purchase(self, item):
        price = self.price(item)
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
        self.messages.append(Message(
            type="purchase",
            subject=subject,
            msgHTML=msgHTML,
            msgPlain=msgPlain)
        )


class RFID_key(Base):
    """RFID_key Class for the Coffee Machine Account System

    ...
    Attributes
    ----------
    __tablename__: str
        tablename for sqlalchemy
    id: int
        sqlalchemy row ID. Autoincremented.
    rfid_key: int
        user's rfid key. Unique.
    user_id: int
        User's ID from User class.
    user: relationship
        Setting up one to many referential relationship between classes.

    """
    __tablename__ = 'rfid_keys'
    id = Column(Integer, primary_key=True)
    rfid_key = Column(Integer, unique=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='rfid_key')


class Message(Base):
    """Message Class for the Coffee Machine Account System

    ...
    Attributes
    ----------
    __tablename__: str
        tablename for sqlalchemy
    id: int
        sqlalchemy row ID. Autoincremented.
    type: str
        Type of message.
    timestamp: datetime
        Time message sent. Datetime object. Autogenerated.
    user_id: int
        User ID that message was sent to.
    subject: str
        Subject line of email.
    msgHTML: str
        HTML text of email.
    msgPlain: str
        Plain text email.
    user: User
        Sets up one to many relatonship between classes.
    """
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    subject = Column(String)
    msgHTML = Column(String)
    msgPlain = Column(String)
    user = relationship('User', back_populates='messages')


class Role(Base):
    """Role Class for the Coffee Machine Account System

    ...
    Attributes
    ----------
    __tablename__: str
        tablename for sqlalchemy
    id: int
        sqlalchemy row ID. Autoincremented.
    user_id: int
        User's ID who has the role.
    name: str
        Name of the role. "Manager", etc.
    permissions: boolean
        Whether the role should have full privileges.
    user: User
        Reference to User class.
    items: Item
        One to many relationship to items class.

    Methods
    -------
    price(str)
        Returns the price of the given item name.
    add_item(str, float)
        Adds an item and a price to the role.
    update_item(str, float)
        Updates an item's price.
    """
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String)
    permissions = Column(Boolean)
    user = relationship('User', back_populates='role')
    items = relationship('Item')

    def price(self, purchase):  # TODO: Make this nicer.
        for item in self.items:
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
    """Item Class for the Coffee Machine Account System

    ...
    Attributes
    ----------
    __tablename__: str
        tablename for sqlalchemy
    id: int
        sqlalchemy row ID. Autoincremented.
    name: str
        Name of the item.
    role: Int
        Back referential relationship to the Role class.
    price: float
        Price of the item.
    """
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(Integer, ForeignKey('role.id'))
    price = Column(Float(precision=2))


class Transaction(Base):
    """Transaction Class for the Coffee Machine Account System

    ...
    Attributes
    ----------
    __tablename__: str
        sqlalchemy table name
    id: int
        sqlalchemy row ID. Autoincremented.
    user_id: int
        User ID that made the transaction.
    timestamp: DateTime
        DateTime object. Autogenerated.
    amount: Float
        Amount the transaction is for.
    user
        Back referential relationship for the User's one to many relationship.
    """
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    amount = Column(Float(precision=2))
    user = relationship('User', back_populates='transactions')

###############################################################


def add_item(item, price):
    """Adds a new item to all roles.

    Parameters
    ----------

    item: str
        The new item's name.
    price: float
        The new item's default price.

    Returns
    -------

    [None]"""

    for role in session.query(Role):
        role.add_item(item, price)


def fingerprint_return_user(fingerprint):
    for user in session.query(User).filter_by(fingerprint=fingerprint):
        return user


def rfid_return_user(rfid_key):

    for user in session.query(User).filter_by(rfid_key=rfid_key):
        return user


def create_user(rfid_key):
    display("Please scan your\n fingerprint.")
    # fingerprint input, assign to slot
    fingerprint = int()
    # Fingerprint failover:
    if fingerprint_slots_used() > 250:
        inactive_user = most_inactive_user()
        slot = inactive_user.fingerprint
        inactive_user.fingerprint = None

    # Clear that fingerprint slot.

    new_user = User(
        rfid_key=rfid_key,
        username=None,
        email=None,
        disabled=0,
        fingerprint=fingerprint
    )

    for _ in range(30):
        new_user.transactions.append(random.randrange(-5, 5))

    session.add(new_user)
    session.commit()
    return new_user


def flag_delinquent():  # figure out a better way to integrate this
    for user in session.query(User):
        user.active = user.active_test()


def fingerprint_slots_used():
    for user in session.query(User).order_by(desc(User.fingerprint)).limit(1):
        return user.fingerprint


def most_inactive_user():
    oldest_user = None
    oldest_timestamp = datetime.today()
    for user in session.query(User):
        for transaction in user.transactions:
            timestamp = transaction.timestamp
            print((oldest_timestamp - timestamp).seconds)
            if (oldest_timestamp - timestamp).seconds > 0:
                oldest_user = user
                oldest_timestamp = timestamp

    return oldest_user


def invoice_users():
    for user in session.query(User):
        user.invoice()


Base.metadata.create_all(engine)


test_user = User(rfid_key=113815, disabled=False)
test_user.username="jschmitz2"
test_user.email="jschmtiz2@hawk.iit.edu"
test_user.disabled=True
test_user.transactions.append(Transaction(amount=0.5))

session.add(test_user)
user = rfid_return_user(113815)
user.role = Role(name="user",permissions=0)
user.role.add_item("coffee", .5)


user.purchase("coffee")

for x in range(10):
    user.purchase("coffee")

user.email="jschmitz2@hawk.iit.edu"
user.history()

session.commit()

print(most_inactive_user().username)
