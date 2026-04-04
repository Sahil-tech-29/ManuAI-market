from database import db 

class User(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(200) , nullable = False)
    email = db.Column(db.String(200) ,nullable = False ,unique = True)
    password = db.Column(db.String(200) ,nullable = False)
    role = db.Column(db.String(50),nullable = False)


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(300))
    description = db.Column(db.String(1000), nullable=False)

    price = db.Column(db.Float)
    manufacturing_cost = db.Column(db.Float)
    delivery_time = db.Column(db.Integer)

    manufacturing_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    manufacturer = db.relationship('User', backref='products')

    category = db.Column(db.String(100))

    image1 = db.Column(db.String(200))
    image2 = db.Column(db.String(200))
    image3 = db.Column(db.String(200))
    image4 = db.Column(db.String(200))



class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    user_name = db.Column(db.String(100))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    quantity = db.Column(db.Integer, default=1)

    product = db.relationship('Product')

    @property
    def subtotal(self):
        return self.product.price * self.quantity

class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    total_price = db.Column(db.Float)
    address = db.Column(db.Text)
    payment_method = db.Column(db.String(50))



class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    manufacturer_id = db.Column(db.Integer)  

    product = db.relationship('Product')