from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from .. import database, models, schemas, oauth2
router = APIRouter(
    prefix='/vote',
    tags=['Vote']
)

# @router.post('/', status_code=status.HTTP_201_CREATED)
# def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends
#          (oauth2.get_current_user)):
    
#     vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
#     found_vote = vote_query.first()


#     if (vote.dir == 1):
#         if found_vote:
#             raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        
#         new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
#         db.add(new_vote)
#         db.commit()
#         return {"message": "Successfully added vote"}
        
#     else: 
#         if not found_vote:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote with {vote.post_id} is not found")
        
#         vote_query.delete(synchronize_session=False)
#         db.commit()

#         return {"message": "Successfully deleted a vote"}
    

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends
         (oauth2.get_current_user)):
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    found_same_post = db.query(models.Post).filter(models.Post.id == vote.post_id, models.Post.owner_id == current_user.id).first()

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {vote.post_id} does not exist')

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        
        if found_same_post:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Voting on own post: {vote.post_id} is not permited")
        
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
        
    else: 
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote with {vote.post_id} is not found")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully deleted a vote"}