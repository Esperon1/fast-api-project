from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from .. import oauth2
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get('/all', response_model=schemas.PostListWithCounts)  # Because we expect a list of posts as a response.
# @router.get('/all')
def get_all_posts(db: Session = Depends(get_db),
                  limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts_query = db.query(models.Post)
    # total_posts = posts_query.count()
    # # sorted accroding to id in descending order
    # posts = posts_query.filter(models.Post.title.contains(search)).order_by(models.Post.id.desc()).limit(limit).offset(
    #     skip).all()
    # return {"total_posts": total_posts, "posts": posts}

    total_count = db.query(models.Post).count()
    result_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))  # tuple (Post, votes)

    result = result_query.filter(models.Post.title.contains(search)
                                 ).order_by(models.Post.id.desc()
                                            ).join(models.Vote,
                                                   models.Post.id == models.Vote.post_id,
                                                   isouter=True).group_by(models.Post.id).limit(limit).offset(
        skip).all()
    print()  # Debugging line to check the result

    return {"total_posts": total_count, "posts": result}


@router.get('/all/{id}', response_model=schemas.PostListWithVotes)
def get_all_posts_id(id: int, db: Session = Depends(get_db)):
    if id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid post ID. ID must be a positive integer.")
    post_query = db.query(models.Post).filter(
        models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    return {"Post": post, "votes": db.query(models.Vote).filter(models.Vote.post_id == id).count()}


@router.get('/latest', response_model=schemas.PostResponse)
def get_latest_post(db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).order_by(models.Post.id.desc()).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No posts available")
    return post


@router.get('/', response_model=List[schemas.PostResponse])  # Because we expect a list of posts as a response.
def get_post_user(db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user),
                  limit: int = 10):
    posts = db.query(models.Post).order_by(models.Post.id.desc()).filter(models.Post.owner_id == current_user.id).limit(
        limit).all()
    return posts


@router.get('/{id}', response_model=schemas.PostResponse)
def get_post_user_id(id: int, db: Session = Depends(get_db),
                     current_user: int = Depends(oauth2.get_current_user)):
    if id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid post ID. ID must be a positive integer.")
    post_query = db.query(models.Post).filter(
        models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to access this post")
    return post


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.model_dump())
    owner_id = current_user.id
    new_post.owner_id = owner_id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # to get the new post with id and created_at
    return new_post


@router.put('/{id}', response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to update this post")

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to delete this post")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
