from scrapy.utils.project import get_project_settings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy import Integer, String, Text, Boolean

DeclarativeBase = declarative_base()


def db_connect():
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


class Product(DeclarativeBase):
    __tablename__ = "rhinoda_products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    image_url = Column(String)
    price = Column(Integer)
    attributes = Column(Text)
    sku = Column(Integer, unique=True)
    category_id = Column(Integer, ForeignKey('rhinoda_categories.id'))
    category = relationship('Category', uselist=True)
    is_updated = Column(Boolean, default=0)


class Category(DeclarativeBase):
    __tablename__ = "rhinoda_categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    parent_category_id = Column(Integer, ForeignKey('rhinoda_categories.id'))
