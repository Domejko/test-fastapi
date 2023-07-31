from fastapi import status, HTTPException, Response, APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2


router = APIRouter(prefix='/vote', tags=['Votes'])

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    if not db.query(models.Post).filter(models.Post.id == vote.post_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post does not exist.')

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()


    if vote.post_dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User {current_user.id} has already voted on this post.')
        
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()

        return {'message': 'Added vote.'}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vote does not exist.')
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {'message': 'Successfuly deleted vote.'}
    