from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Integer,Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData

DATABASE_NAME = 'spamno'

engine = create_engine('sqlite:///sqlite3.db')

Base = declarative_base()
metadata_obj = MetaData()

Session = sessionmaker(bind=engine)

session = Session()

user = Table(
    "user",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_name", String(100), nullable=False),
    Column("phone_number", String(100)),
    Column('user_id', String(100)),
    Column('id_chat', String(100)),
    Column('id_users', String(100))
)


class User(Base):

  __tablename__ = 'user'

  id = Column(Integer, primary_key=True)
  user_name = Column(String(100))
  phone_number = Column(String(100))
  user_id = Column(String(100))
  id_chat = Column(String(100))
  id_users = Column(String(100))

  def update_name(id_to_update, new_desc):
    try:
        query = session.query(User).filter(User.user_name == id_to_update).\
            update({User.user_name: new_desc}, synchronize_session=False)
        session.commit()
    except:
        session.rollback()
  
  def update_phone(id_to_update, new_desc):
    try:
        query = session.query(User).filter(User.user_name == id_to_update).\
            update({User.phone_number: new_desc}, synchronize_session=False)
        session.commit()
    except:
        session.rollback()

def creates(what):
  try:
    what.create(engine)
  except:
    return ''

creates(user)
