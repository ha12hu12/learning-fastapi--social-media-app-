from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from .. import models, schemas, oauth2
from typing import List, Optional



router = APIRouter(
    prefix="/posts",
    tags=["Post Control"])

#get all posts
@router.get("/", response_model=List[schemas.PostVote])
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10,
              skip: int = 0,
              search: Optional[str] = ""
              ):

    results = (
        db.query(
            models.Post,
            func.count(models.Vote.post_id).label("votes")
        )
        .join(
            models.Vote,
            models.Vote.post_id == models.Post.id,
            isouter=True
        )
        .group_by(models.Post.id)
    ).filter(
        models.Post.title.contains(search)
    ).limit(
        limit
    ).offset(
            skip
        ).all()

    return results

#get one post by id

@router.get("/{id}", response_model=schemas.PostVote)
def get_post(id: int, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(
        models.Post, func.count(models.Vote.post_id).label("votes")
        ).join(
            models.Vote, models.Vote.post_id == models.Post.id,
            isouter=True
        ).group_by(
            models.Post.id
        ).filter(
            models.Post.id == id
        ).first()

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            f"Post with id: {id} does not exist")

    return post

#Create post
@router.post("/", response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    print(current_user)
    new_post = models.Post(owner_id=current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

#Delete post
@router.delete("/{id}", response_model=schemas.PostResponse)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(
        models.Post
        ).filter(
            models.Post.id == id)
    
    post = post_query.first()

    if not post:
        raise HTTPException(404, f"Post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(403, f"You dont own this post to be able to delete it you monster")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=204)

#Update post
@router.put("/{id}", response_model=schemas.PostResponse)
def updated_post(updated_post: schemas.PostCreate, id: int, 
                  db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(
        models.Post
    ).filter(
        models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(404, f"Post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(403, f"You dont own this post to be able to delete it you monster")

    post_query.update(updated_post.dict())

    return post_query.first()
