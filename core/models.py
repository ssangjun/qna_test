from sqlalchemy     import Column, ForeignKey, Integer, String, Boolean, Text, DECIMAL, TIMESTAMP, func, text
from sqlalchemy.orm import relationship, backref

from .database      import Base

class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    email      = Column(String(200), unique=True, nullable=False)
    password   = Column(String(150), nullable=False)
    is_valid   = Column(Boolean, default=True)
    first_name = Column(String(50), nullable=True)
    last_name  = Column(String(50), nullable=True)
    auth_code  = Column(String(10), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    _users_paragraphs       = relationship("Paragraph", secondary="users_paragraphs_videos", back_populates="_users", viewonly=True)
    _users_videos           = relationship("Video", secondary="users_paragraphs_videos", back_populates="_users", viewonly=True)
    _users_videoproducers   = relationship("VideoProducer", secondary="users_videoproducers", back_populates="_users", viewonly=True)
    _users_social_platforms = relationship("Social_Platform", secondary="users_social_platforms", back_populates="_users", viewonly=True)

class Social_Platform(Base):
    __tablename__ = "social_platforms"

    id   = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=True)
    name = Column(String(50))

    _users = relationship("User", secondary="users_social_platforms", back_populates="_users_social_platforms", viewonly=True)

class User_Social_Platform(Base):
    __tablename__ = "users_social_platforms"

    id                 = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=True)
    user_id            = Column(Integer, ForeignKey("users.id"))
    social_platform_id = Column(Integer, ForeignKey("social_platforms.id"))
    access_token       = Column(String(300))
    refresh_token      = Column(String(300))

class SearchHistory(Base):
    __tablename__ = "searchhistories"

    id         = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    log        = Column(Text, nullable=False)
    user_id    = Column(Integer, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    user = relationship("User", order_by="User.id")

class Project(Base):
    __tablename__ = "projects"

    id         = Column(String(200), primary_key=True, index=True, nullable=False)
    title      = Column(String(100), nullable=False)
    user_id    = Column(Integer, ForeignKey("users.id"))
    script_id  = Column(Integer, ForeignKey("scripts.id"))
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    user   = relationship("User", order_by="User.id")
    script = relationship("Script", order_by="Script.id")

class Script(Base):
    __tablename__ = "scripts"

    id         = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    title      = Column(String(50), nullable=False)
    user_id    = Column(Integer, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    user = relationship("User", order_by="User.id")

class Paragraph(Base):
    __tablename__ = "paragraphs"

    id         = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    sequence   = Column(Integer, nullable=False)
    contents   = Column(String(2000), nullable=False)
    script_id  = Column(Integer, ForeignKey("scripts.id"))
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    script        = relationship("Script", order_by="Script.id")
    _keywords     = relationship("Keyword", secondary="paragraphs_keywords", back_populates="_paragraphs")
    _videos       = relationship("Video", secondary="paragraphs_videos", back_populates="_paragraphs")
    _users_videos = relationship("Video", secondary="users_paragraphs_videos", back_populates="_users_paragraphs", viewonly=True)
    _users        = relationship("User", secondary="users_paragraphs_videos", back_populates="_users_paragraphs", viewonly=True)

class Keyword(Base):
    __tablename__ = "keywords"

    id         = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    contents   = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    _paragraphs = relationship("Paragraph", secondary="paragraphs_keywords", back_populates="_keywords")
    _videos    = relationship("Video", secondary="keywords_videos", back_populates="_keywords")

class Paragraph_Keyword(Base):
    __tablename__ = "paragraphs_keywords"

    id           = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    paragraph_id = Column(Integer, ForeignKey("paragraphs.id"))
    keyword_id   = Column(Integer, ForeignKey("keywords.id"))

class Paragraph_Video(Base):
    __tablename__ = "paragraphs_videos"
    
    id           = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    paragraph_id = Column(Integer, ForeignKey("paragraphs.id"))
    video_id     = Column(Integer, ForeignKey("videos.id"))

class User_Paragraph_Video(Base):
    __tablename__ = "users_paragraphs_videos"

    id              = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    user_id         = Column(Integer, ForeignKey("users.id"))
    paragraph_id    = Column(Integer, ForeignKey("paragraphs.id"))
    video_id        = Column(Integer, ForeignKey("videos.id"))
    choice_status   = Column(Boolean, default=False)
    edit_start_time = Column(String(50))
    edit_end_time   = Column(String(50))

    paragraph = relationship("Paragraph")
    video     = relationship("Video")

class Keyword_Video(Base):
    __tablename__ = "keywords_videos"

    id          = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    keyword_id  = Column(Integer, ForeignKey("keywords.id"))
    video_id    = Column(Integer, ForeignKey("videos.id"))

class Video(Base):
    __tablename__ = "videos"

    id                = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    videoURL          = Column(String(200), unique=True, nullable=False)
    contract_status   = Column(Boolean, default=False)
    video_resource_id = Column(String(200), unique=True)
    videoproducer_id  = Column(Integer, ForeignKey("videoproducers.id"))
    authorship_id     = Column(Integer, ForeignKey("authorships.id"), nullable=True)
    thumbnails        = Column(String(400))
    created_at        = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at        = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    videoproducer     = relationship("VideoProducer", order_by="VideoProducer.id")
    authorship        = relationship("Authorship", order_by="Authorship.id")
    _paragraphs       = relationship("Paragraph", secondary="paragraphs_videos", back_populates="_videos")
    _users_paragraphs = relationship("Paragraph", secondary="users_paragraphs_videos", back_populates="_users_videos", viewonly=True)
    _users            = relationship("User", secondary="users_paragraphs_videos", back_populates="_users_videos", viewonly=True)
    _keywords         = relationship("Keyword", secondary="keywords_videos", back_populates="_videos")

class VideoProducer(Base):
    __tablename__ = "videoproducers"

    id   = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    name = Column(String(50), nullable=False)

    _users = relationship("User", secondary="users_videoproducers", back_populates="_users_videoproducers")

class User_VideoProducer(Base):
    __tablename__ = "users_videoproducers"

    id               = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    access_token     = Column(String(500))
    user_id          = Column(Integer, ForeignKey("users.id"))
    videoproducer_id = Column(Integer, ForeignKey("videoproducers.id"))

class Subscription(Base):
    __tablename__ = "subscriptions"

    id          = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    tier        = Column(String(50), nullable=False)
    description = Column(String(100), nullable=False)
    price       = Column(DECIMAL, nullable=False)

class PaymentMethod(Base):
    __tablename__ = "paymentmethods"

    id     = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    method = Column(String(50), nullable=False)

class Payment(Base):
    __tablename__ = "payments"

    id               = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    user_id          = Column(Integer, ForeignKey("users.id"))
    subscription_id  = Column(Integer, ForeignKey("subscriptions.id"))
    paymentmethod_id = Column(Integer, ForeignKey("paymentmethods.id"))
    created_at       = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at       = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    user          = relationship("User", order_by="User.id")
    subscription  = relationship("Subscription", order_by="Subscription.id")
    paymentmethod = relationship("PaymentMethod", order_by="PaymentMethod.id")

class Authorship(Base):
    __tablename__ = "authorships"
    
    id         = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    name       = Column(String(100))
    email      = Column(String(200))
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

class ExceededYoutubeQuota(Base):
    __tablename__ = "exceeded_youtube_quota"

    id         = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    user_id    = Column(ForeignKey("users.id"))
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

class UserDownloadHistory(Base):
    __tablename__ = "users_download_histories"

    id         = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    user_id    = Column(ForeignKey("users.id"), nullable=False)
    video_id   = Column(ForeignKey("videos.id"), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    path       = Column(String(150), nullable=False)

    user  = relationship("User", order_by="User.id")
    video = relationship("Video", order_by="Video.id")


class Admin(Base):
    __tablename__ = "admins"

    id             = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    admin_account  = Column(String(25), unique=True, nullable=False)
    admin_password = Column(String(150), nullable=False)
    admin_type     = Column(String(25), nullable=False)
    created_at     = Column(TIMESTAMP, server_default=func.now(), nullable=False)
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