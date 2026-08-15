from sqlalchemy import Column,String,Integer
from db import Base

class Game(Base):
    __tablename__="game"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    genre = Column(String)
    image = Column(String)

    