from .database import Base
from sqlalchemy import Column, Integer, Text, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .utils import pwd_context


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    posts = relationship("Post", back_populates="user")
    phone_number = Column(String, nullable=True)

    def set_password(self, password):
        self.password = pwd_context.hash(password)

    def check_password(self, password):
        return pwd_context.verify(password, self.password)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    is_published = Column(Boolean, server_default="False", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()') )
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="posts")


class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
