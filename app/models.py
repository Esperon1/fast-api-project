from sqlalchemy import Column, String, Numeric, TIMESTAMP, Text, Boolean, ForeignKey, BIGINT
from sqlalchemy.orm import relationship

from .database import Base
from sqlalchemy.sql import func


class Post(Base):
    __tablename__ = "posts"

    id = Column(BIGINT, primary_key=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)  # Text type for larger content
    published = Column(Boolean, nullable=False,
                       server_default="1")  # Using BIGINT to represent boolean (1 for True, 0 for False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    rating = Column(Numeric(5, 2), nullable=True)
    # Foreign key
    owner_id = Column(BIGINT, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")  # Establish relationship with User model defined in schemas.py


class User(Base):
    __tablename__ = "users"

    id = Column(BIGINT, primary_key=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())


class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(BIGINT, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    post_id = Column(BIGINT, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)
