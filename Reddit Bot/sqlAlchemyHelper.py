# Python script to help explore SQLAlchemy and our database
from sqlalchemy import *
import time

# The engine is the core interface to the database
engine = create_engine('mysql://rancheta_dwaxe:fsa7ya@rafaelancheta.com:80/rancheta_icheckbooks', echo=True)

# Create a metadata catalog with user and address tables
metadata = MetaData()
users = Table('users', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', String),
	Column('fullname', String),
)
addresses = Table('addresses', metadata,
	Column('id', Integer, primary_key=True),
	Column('user_id', None, ForeignKey('users.id')),
	Column('email_address', String, nullable=False)
)

# Create our selection of tables inside the database
metadata.create_all(engine)

# An insert construct represents an INSERT statement
ins = users.insert().values(name='jack', fullname='Jackaloupe')

# Connect the engine to the database and execute ins
conn = engine.connect()
result = conn.execute(ins)

# Terser
ins = users.insert()
conn.execute(ins, id=2, name='wendy', fullname='Wendigo')

# Dictionary insert
conn.execute(addresses.insert(), [
    {'user_id': 1, 'email_address' : 'jack@yahoo.com'},
    {'user_id': 1, 'email_address' : 'jack@msn.com'},
    {'user_id': 2, 'email_address' : 'www@www.org'},
    {'user_id': 2, 'email_address' : 'wendy@aol.com'},
])

# Selection
s = select([users])
result = conn.execute(s)

# Prints tuples
# for row in result:
# 	print(row)

# Dictionary indices work too
row = result.fetchone()
print('name: ', row['name'], '; fullname: ', row['fullname'])
print('id: ', row[0], 'name: ', row[1], '; fullname: ', row[2])

# Another way is to use the column objects as keys
print('name: ', row[users.c.name])

# Close sets which have pending rows remaining
result.close()