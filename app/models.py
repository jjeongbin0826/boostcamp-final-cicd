from sqlalchemy import Column, String, BigInteger, ForeignKey, DateTime, Date, UniqueConstraint, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "member"

    member_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    nickname = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), nullable=True)
    birth_date = Column(Date, nullable=True) 
    gender = Column(String(10), nullable=True) 
    profile_image = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    social_accounts = relationship("UserSocialAccount", back_populates="user")
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")


class UserSocialAccount(Base):
    __tablename__ = "social_account"
    
    social_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    member_id = Column(BigInteger, ForeignKey("member.member_id"), nullable=False)
    provider_name = Column(String(20), nullable=False) # google, naver 등
    provider_user_identifier = Column(String(255), nullable=False) # 소셜 고유 ID
    email = Column(String(255), nullable=True)

    user = relationship("User", back_populates="social_accounts")

    __table_args__ = (
        UniqueConstraint("provider_name", "provider_user_identifier", name="uq_social_provider"),
    )


class Product(Base):
    __tablename__ = "product"

    product_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    product_name = Column(String(50), nullable=False)
    ticker = Column(String(20), nullable=False, unique=True)

    prices = relationship("DailyPrice", back_populates="product", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="product", cascade="all, delete-orphan")
    news_list = relationship("News", back_populates="product", cascade="all, delete-orphan")


class DailyPrice(Base):
    __tablename__ = "daily_price"

    price_id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True)
    product_id = Column(BigInteger, ForeignKey("product.product_id", ondelete="CASCADE"), nullable=False)
    base_date = Column(DateTime, nullable=False)
    closing_price = Column(Float, nullable=False)
    prev_closing_price = Column(Float, nullable=False)
    price_change = Column(Float, nullable=False)
    change_rate = Column(Float, nullable=False)

    product = relationship("Product", back_populates="prices")
    
    
class Favorite(Base):
    __tablename__ = "favorite"

    member_id = Column(BigInteger, ForeignKey("member.member_id", ondelete="CASCADE"), primary_key=True, nullable=False)
    product_id = Column(BigInteger, ForeignKey("product.product_id", ondelete="CASCADE"), primary_key=True, nullable=False)

    product = relationship("Product", back_populates="favorites")
    user = relationship("User", back_populates="favorites")
    
    
class News(Base):
    __tablename__ = "news"

    news_id = Column(BigInteger, primary_key=True, autoincrement=True)
    product_id = Column(BigInteger, ForeignKey("product.product_id", ondelete="CASCADE"), nullable=False)
    
    title = Column(String(255), nullable=False)
    news_url = Column(String(255), nullable=False)
    site_name = Column(String(255), nullable=False)
    published_at = Column(DateTime, nullable=False) 

    product = relationship("Product", back_populates="news_list")