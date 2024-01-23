from .. import models, schemas
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import FastAPI, status, HTTPException, Depends, Response, APIRouter
from ..database import get_db
from typing import Optional, List
from .. import oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostOut]) # List is used to specify that schemas.Post will have list of posts as response. 
# @router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int = 
                 Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")
                       ).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True
                              ).group_by(models.Post.id
                                         ).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = 
                 Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING* """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    # conn.commit()
    print(current_user.id)

    new_post = models.Post(owner_id=current_user.id, **dict(post))

    
    db.add(new_post) # This is to add new post to the db
    db.commit() # This is to comnit the changes in db
    db.refresh(new_post) # This is to show the new_post in response
    
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = 
                 Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * from posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")
                       ).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True
                              ).group_by(models.Post.id
                                         ).filter(models.Post.id == id).first()


    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} was not found")
    return post
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = 
                 Depends(oauth2.get_current_user)): 

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING* """, (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id) #This is query but not actual the post. we used .first() to get the post in if statement down
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = 
                 Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING* """,
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()


    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    

    post_query.update(dict(updated_post), synchronize_session=False)
    db.commit()
    
    return post_query.first()