from sqlalchemy import *

engine = create_engine('mysql://root:@localhost/food_securitydb')

metadata_obj = MetaData()

user = Table('user', metadata_obj,
    Column('user_id', Integer, primary_key=True),
    Column('user_name', String(16), nullable=False),
    Column('email_address', String(60), key='email'),
    Column('nickname', String(50), nullable=False)
)

user_prefs = Table('user_prefs', metadata_obj,
    Column('pref_id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey("user.user_id"), nullable=False),
    Column('pref_name', String(40), nullable=False),
    Column('pref_value', String(100))
)

metadata_obj.create_all(engine)