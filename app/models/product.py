from typing import List

from app import db, ma


class ProductModel(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sku = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    brand = db.Column(db.String(50))
    model = db.Column(db.String(50))
    price = db.Column(db.Float)

    def __repr__(self):
        return f'<Product {self.sku}>'

    @classmethod
    def find_by_id(cls, _id) -> "Product":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_sku(cls, _sku) -> "Product":
        return cls.query.filter_by(sku=_sku).first()

    @classmethod
    def find_all(cls) -> List["Product"]:
        return cls.query.all()


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductModel
        load_instance = True
