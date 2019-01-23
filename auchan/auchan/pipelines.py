# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from auchan.Models import db_connect, Product, Category


class AuchanPipeline(object):
    def __init__(self):
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()

        product = session.query(Product).filter_by(sku=item['sku']).first()
        if product is not None:
            if product.price != item['price']:
                product.price = item['price']
                product.is_updated = True
                session.add(product)
                session.commit()
            return

        product = Product()
        product.name = item['name']
        product.description = item['description']
        product.image_url = item['image_url']
        product.price = item['price']
        product.attributes = item['attributes']
        product.sku = item['sku']

        # Create categories
        parent_cat_id = None
        for category_name in item['categories']:
            cat = session.query(Category).filter_by(name=category_name).first()

            if cat is None:
                category = Category()
                category.name = category_name
                category.parent_category_id = parent_cat_id
                session.add(category)
                session.flush()

                parent_cat_id = category.id
            else:
                parent_cat_id = cat.id

        try:
            product.category_id = parent_cat_id
            session.add(product)
            # product.category.append(category)

            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
