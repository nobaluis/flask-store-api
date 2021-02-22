from typing import List

from app import db, ma


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(10))
    email = db.Column(db.String(50))
    address = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(5))
    stocks = db.relationship('StockModel', backref="store", lazy=True)

    def __repr__(self):
        return f'<Store {self.id}>'

    @classmethod
    def find_by_id(cls, _id) -> "Store":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["Store"]:
        return cls.query.all()


class StoreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StoreModel
        load_instance = True
