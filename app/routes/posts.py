
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import model
from .. database import get_db
from .. oauth2 import get_current_user
from .. schemas import PostCreate, PostOut

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[PostOut])
def get_posts(db: Session = Depends(get_db),current_user: model.User = Depends(get_current_user)):
    return (
        db.query(model.Post)
        .filter(model.Post.published.is_(True))
        .all()
    )


@router.get("/{post_id}", response_model=PostOut)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    post = db.get(model.Post, post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    if not post.published:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    return post


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PostOut,
)
def create_post(
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    new_post = model.Post(
        **post_data.model_dump(),
        user_id=current_user.id,
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.put("/{post_id}", response_model=PostOut)
def update_post(
    post_id: int,
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    post = db.get(model.Post, post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post",
        )

    for key, value in post_data.model_dump().items():
        setattr(post, key, value)

    db.commit()
    db.refresh(post)

    return post


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    post = db.get(model.Post, post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post",
        )

    db.delete(post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)