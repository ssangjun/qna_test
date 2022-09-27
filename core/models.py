from sqlalchemy     import Column, ForeignKey, Integer, String, func, text, TIMESTAMP
from sqlalchemy.orm import relationship, backref

from .database      import Base

class Admin(Base):
    __tablename__ = "admins"

    id             = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    admin_account  = Column(String(25), unique=True, nullable=False)
    admin_password = Column(String(150), nullable=False)
    admin_type     = Column(String(25))
    created_at     = Column(TIMESTAMP, server_default=func.now())
    updated_at     = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

class Post(Base):
    __tablename__ = "posts"

    id         = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    nickname   = Column(String(20), nullable=False)
    password   = Column(String(30), nullable=False)
    title      = Column(String(100), nullable=False)
    content    = Column(String(1000), nullable=False)

    # post_set = relationship("File", backref=backref("post"))

class Comment(Base):
    __tablename__ = "comments"

    id         = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    admin_id   = Column(ForeignKey("admins.id"), nullable=False)
    post_id    = Column(ForeignKey("posts.id"), nullable=False)
    content    = Column(String(1000), nullable=False)


class File(Base):
    __tablename__ = "files"

    id         = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    post_id    = Column(ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    file_url   = Column(String(150), nullable=False)

    post = relationship("Post", backref=backref("post_set", cascade="delete"))

class Notice(Base):
    __tablename__ = "notices"

    id         = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    admin_id   = Column(ForeignKey("admins.id"), nullable=False)
    title      = Column(String(100), nullable=False)
    content    = Column(String(1000), nullable=False)