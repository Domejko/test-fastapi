from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    # PrimaryKeyConstraint(id)


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, nullable=False, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP, onupdate=text('now()'), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE')
    # PrimaryKeyConstraint(id)

    owner = relationship('User')
    

class Vote(Base):
    __tablename__ = 'votes'
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    # ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE')
    # ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE')
    # PrimaryKeyConstraint(post_id, user_id)
