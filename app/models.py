from app import db

class Clothes(db.Model):
    __tablename__ = 'clothes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(50))
    brand = db.Column(db.String(50))
    material = db.Column(db.String(100))
    description = db.Column(db.String(255))
    is_available = db.Column(db.Boolean, default=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    rating = db.Column(db.Float, default=0.0)

    category = db.relationship('Category', back_populates='clothes')


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    clothes = db.relationship('Clothes', back_populates='category')
