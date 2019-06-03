from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Connecting to the engine with PostgreSQL (make sure psycopg2 is installed!):
engine = create_engine('postgresql://user:password@server_ip/database_name')

# The declarative_base() base class:
    # Contains a MetaData object where Table objects are collected.
    # This is used to issue create statements from the stored metadata.

Base = declarative_base()
Base.metadata.create_all(engine)

    # Alternatively, use it to import existing metadata:

Base = declarative_base(metadata=mymetadata)

# Requirements of table:
    # __tablename__ to be set
    # At least one primary_key column


##########################################
# Creating tables
##########################################


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True),
    name = Column(String)

# __init__ methods are created automatically that accept keyed parameters

##########################################
# Inserting Data
##########################################

dave_user = User(name="Dave")

# Creating a session:
session = sessionmaker(bind=engine)

# Adding objects to the session:
session.add(dave_user)

# Queries can be run on data, even before it's committed:

our_user = session.query(User).filter_by(name="Dave").first()
our_user is dave_user
    # True

# Multiple users can be added simultaneously:
session.add_all([
    User(name="Wendy"),
    User(name="Steven"),
    User(name="Donald")
    ])

# Since we haven't committed yet, we can change informaton to be entered
# by just changing the referenced objects:

dave_user.name = "David" # This will change the item input into the engine

session.commit()

# Now that we've committed, we can look at the ID objects from these:
dave_user.id
# Would return integer 1.

##########################################
# Rolling back transactions
##########################################

session.rollback()

# This rolls back non-committed transactions

##########################################
# Querying data
##########################################

# Query objects are created by using [Session].query().
# Arguments: any number of classes and class-instrumented descriptors.

# When evaluated in an iterative context, a list of objects present is returned.

for instance in session.query(User).order_by(User.id):
    print(instance.name, instance.id)

# The Query object also accepts ORM descriptors as arguments.

# When multipe class or column-based entities are expressed as aruguments, the return
# function is a tuple.

for name, fullname in session.query(User.name, User.fullname):
    print(name, fullname)

# Limit and offset can be accomplished using python slice notion. Make sure
# to specify an ordering, or else the returned values will be somewhat random.

for u in session.query(User).order_by(user.id)[1:3]:
    print(u)
# <User(name='wendy', fullname='Wendy Williams', nickname='windy')>

# Filtering results can be acomplished by two methods:

# filter_by():

for name, in session.query(User.name).filter_by(fullname='Ed Jones'):
    print(name)

# Or filter(), which allows you to use more flexible python class-level filtering:

for name, in session.query(User.name).filter(User.fullname='Ed Jones'):
    print(name)


# Query object is generative, meaning filter calls and other similar return
# another query object, so you can stack filters (represented in SQL with an AND).

# Common filter operators:

query.filter(User.name == 'ed')
query.filter(User.name != 'ed')
query.filter(User.name.like('%ed%'))
query.filter(User.name.ilike('%ed%')) # Case insensitive like.
query.filter(User.name.in_(['ed', 'wendy'])) # in
query.filter(~User.name.in_(['ed', 'wendy'])) # NOT in.
query.filter(User.name == None) # is null
query.filter(User.name != None) # is not null

from sqlalchemy import and_, or_
query.filter(or_(User.name == 'ed', User.name == 'wendy'))

# Returning lists and scalars:

query = session.query(User).filter(User.name.like('%ed%'))

query.all()
# Returns a list
query.first()
# Applies a limit of one, and returns the first result as a scalar
query.one() # Fully fetches al rows, and if not exactly one object matches,
# raises an error.
query.one_or_none()
# Like one, but it's fine with none.
query.scalar()
# Invokes one() method, then returns the first column of the row.

##########################################
# Querying data - Using Textual SQL
##########################################

from sqlalchemy import text
for user in session.query(user).filter(text("id<224")).order_by(text("id")).all():
    print(user.name)

# Further use of straight textual SQL can be done.
# Bound parameters can be specified using a colon, and then the params() method.

session.query(User).filter(text("id<:value and name=:name")).params(value=224, name='fred').order_by(User.id).one()

##########################################
# Querying data - Other Methods
##########################################

# Counting how many objects a SQL query would return:
session.query(User).filter(User.name.like('%ed')).count()

# When the 'thing to be counted' needs to be specifically indicated, we can use the 'count' function
# from func.count().

from sqlalchemy import func

session.query(func.count(User.name), User.name).group_by(User.name).all()

##########################################
# Building a relationship between tables
##########################################

# See: https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#relationship-patterns


from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id')) # Restricts values in this Column
    # to be only those that are in the 'id' column of users

    user = relationship("user", back_populates("addresses"))

User.addresses = relationship( # Uses foreign key relationships to determine that Address.user will be many to one.
    "Address", order_by=Address.id, back_populates="User")

# Basic overview of relationship types:

# One to many:
# Places foreign key restriction on child table referencing the parent.
# Relationship() is then specified on the parent, referencing a collection of child items.

# Establishing this as a bidirectional relationsihp,
