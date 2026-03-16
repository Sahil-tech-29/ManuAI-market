from database import db 

class User(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(200) , nullable = False)
    email = db.Column(db.String(200) ,nullable = False ,unique = True)
    password = db.Column(db.String(200) ,nullable = False)
    role = db.Column(db.String(50),nullable = False)


class Product(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(200) , nullable = False)
    title = db.Column(db.String(300))
    description = db.Column(db.String(1000) ,nullable = False)
    price = db.Column(db.Float)
    manufacturing_cost = db.Column(db.Float)
    delivery_time = db.Column(db.Integer)
    manufacturing_id = db.Column(db.Integer)
    category = db.Column(db.String(100))
    image1 = db.Column(db.String(200))
    image2 = db.Column(db.String(200))
    image3 = db.Column(db.String(200))
    image4 = db.Column(db.String(200))
