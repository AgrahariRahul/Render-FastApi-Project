from pydantic import BaseModel

class BlogRequest(BaseModel):
    title:str
    content:str
    
    
class BlogResponse(BaseModel):
    id:int
    title:str
    content: str    