from fastapi import status, HTTPException, Response, APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from .. import models, oauth2, schemas, database


router = APIRouter(prefix='/posts', tags=['Posts'])


@router.get('/', response_model=List[schemas.PostOut])
def get_post(skip: int = 0, db: Session = Depends(database.get_db), limit: int = 10, search: Optional[str] = ''):

    posts = db.query(models.Post, func.count(models.Vote.post_id).label('vote_count'))\
                        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
                            .group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = list(map(lambda x:x._mapping,posts))
    
    return posts


@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(database.get_db)):

    returned_post = db.query(models.Post, func.count(models.Vote.post_id).label('vote_count'))\
                        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
                            .group_by(models.Post.id).filter(models.Post.id == id).first()

    if not returned_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')
    
    return returned_post


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(database.get_db)):

    new_post = models.Post(user_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    
    delete_post_query = db.query(models.Post).filter(models.Post.id == id)
    post = delete_post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    
    if current_user.id != post.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Unauthorized to perform requested action.')
    
    delete_post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    update_post_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_update = update_post_query.first()

    if post_to_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    
    if current_user.id != post_to_update.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Unauthorized to perform requested action.')
    
    update_post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post_to_update
