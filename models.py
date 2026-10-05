from sqlalchemy import Column,String, Integer,Text
from database import BASE

class Blog(BASE):
    __tablename__ = "blog"
    
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    content = Column(Text)