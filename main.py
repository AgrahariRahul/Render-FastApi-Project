from fastapi import FastAPI,HTTPException,Depends,Query
import schemas,models,auth
from sqlalchemy.orm import Session
from database import BASE,SessionLocal,engine

models.BASE.metadata.create_all(bind = engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close
        
@app.post("/login")
def login():
    return{
        "access_token" : auth.create_token({"user":"admin"}),
        "token_type":"bearer"
    }        
   
@app.get("/")        
def get_home():
    return {
        "message":"welcome to blog fast api project"
    }
    
@app.post("/blog/create",response_model=schemas.BlogResponse)
def create_blog(blog_req:schemas.BlogRequest,db:Session = Depends(get_db),
                user = Depends(auth.verify_token)):
    new_blog = models.Blog(
         title = blog_req.title,
         content = blog_req.content
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blog/all")
def get_all_blog(db:Session = Depends(get_db),user = Depends(auth.verify_token)):
    query = db.query(models.Blog)
    return query.all()

@app.get("/blog/{blog_id}",response_model=schemas.BlogResponse)
def get_blog(id:int,db:Session = Depends(get_db),user = Depends(auth.verify_token)):
   blog = db.query(models.Blog).filter(models.Blog.id==id).first()
   if not blog:
       raise HTTPException(status_code=404,detail="Id not found")
   return blog

@app.put("/blog/update/{blog_id}")
def update_blog(blog_id:int,blog_req:schemas.BlogRequest,db:Session = Depends(get_db)
                ,user = Depends(auth.verify_token)):
   blog = db.query(models.Blog).filter(models.Blog.id==blog_id).first()
   if not blog:
       raise HTTPException(status_code=404,detail="Id not found")
   blog.title = blog_req.title
   blog.content = blog_req.content
   db.commit()
   db.refresh(blog)
   return blog

@app.delete("/blog/delete/{blog_id}")
def delete_blog(blog_id:int,db:Session = Depends(get_db),user = Depends(auth.verify_token)):
     blog = db.query(models.Blog).filter(models.Blog.id==blog_id).first()
     if not blog:
            raise HTTPException(status_code=404,detail="Id not found")
     db.delete(blog)
     db.commit()
     return{
        "message":"Blog deleted Successfully"
    }  
   
    
            
 