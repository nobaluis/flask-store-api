from typing import List

from app import db, ma


class StockModel(db.Model):
    __tablename__ = 'stocks'

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    quantity = db.Column(db.Integer)

    product = db.relationship('ProductModel', backref=db.backref('stocks', lazy=True))

    def __repr__(self):
        return f"<Stock(product='{self.product.name}', quantity='{self.quantity}')>"

    @classmethod
    def find_by_store(cls, store_id) -> List["Store"]:
        return cls.query.filter_by(store_id=store_id).all()

    @classmethod
    def find_by_product(cls, product_id) -> List["Store"]:
        return cls.query.filter_by(product_id=product_id).all()

    @classmethod
    def find_by_store_and_product(cls, store_id, product_id) -> "Store":
        return cls.query.filter_by(
            store_id=store_id,
            product_id=product_id
        ).first()

    @classmethod
    def find_all(cls) -> List["Store"]:
        return cls.query.all()


class StockSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StockModel
        load_instance = True
