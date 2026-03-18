from flask import Flask,render_template,request,session,redirect,Response
from database import db
from models import User
from models import Product
from models import Review
from models import Cart
from models import Order
from models import OrderItem
import os
from werkzeug.utils import secure_filename
from ai_utils import generate_description,generate_title,generate_keywords,generate_market_analysis,generate_final_price,generate_summary,generate_review_insight
import markdown 
from sqlalchemy import or_


UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


app = Flask(__name__)

app.secret_key = "flask_secretkey"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///manuai.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# Login page route 
@app.route("/", methods=["GET", "POST"])
def home():

    error = None   # 👈 add this

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email, password=password).first()

        if user:
            session["user_id"] = user.id
            session["role"] = user.role
            session["name"] = user.name
            return redirect("/dashboard")
        else:
            error = "Invalid email or password "

    return render_template("index.html", error=error)



# Register page route
@app.route("/register" ,methods = ["GET" ,"POST"])
def register():
    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        new_user = User(
            name = name ,
            email = email ,
            password = password,
            role = role
        )

        db.session.add(new_user)
        db. session.commit()

        return redirect("/")
        
    return render_template("register.html")





# Route to dashboards
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/")

    if session["role"] == "customer":
        return render_template("customer_dashboard.html")

    products = Product.query.filter_by(manufacturing_id=session["user_id"]).all()

    total_products = len(products)

    profits = []
    categories = []

    for p in products:
        if p.price and p.manufacturing_cost:
            profits.append(p.price - p.manufacturing_cost)
        if p.category:
            categories.append(p.category)

    avg_profit = round(sum(profits)/len(profits),2) if profits else 0

    top_category = max(set(categories), key=categories.count) if categories else "None"

    return render_template(
        "manufacture_dashboard.html",
        total_products=total_products,
        avg_profit=avg_profit,
        top_category=top_category
    )



# Route to Upload product page 
@app.route("/upload-product", methods=["GET","POST"])
def upload_product():

    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":

        name = request.form.get("name")
        description = request.form.get("description")
        price = float(request.form.get("price") or 0)
        manufacturing_cost = float(request.form.get("manufacturing_cost") or 0)
        delivery_time = int(request.form.get("delivery_time") or 0)

        category = request.form.get("category")
        title = request.form.get("title")

        if category == "Other":
            category = request.form.get("custom_category")

        image1 = request.files["image1"]
        image2 = request.files.get("image2")
        image3 = request.files.get("image3")
        image4 = request.files.get("image4")

        filename1 = secure_filename(image1.filename)
        image1.save(os.path.join(app.config["UPLOAD_FOLDER"], filename1))

        filename2 = filename3 = filename4 = None

        if image2 and image2.filename != "":
            filename2 = secure_filename(image2.filename)
            image2.save(os.path.join(app.config["UPLOAD_FOLDER"], filename2))

        if image3 and image3.filename != "":
            filename3 = secure_filename(image3.filename)
            image3.save(os.path.join(app.config["UPLOAD_FOLDER"], filename3))

        if image4 and image4.filename != "":
            filename4 = secure_filename(image4.filename)
            image4.save(os.path.join(app.config["UPLOAD_FOLDER"], filename4))

        

        product = Product(
        name=name,
        title=title,
        description=description,
        category=category,
        price=price,
        manufacturing_cost=manufacturing_cost,
        delivery_time=delivery_time,
        manufacturing_id=session["user_id"],
        image1=filename1,
        image2=filename2,
        image3=filename3,
        image4=filename4
    )

        db.session.add(product)
        db.session.commit()

        return redirect("/my-products")

    return render_template("upload_product.html")




#Route to View Products page 
@app.route("/my-products")
def products():

    if "user_id" not in session:
        return redirect("/")
    products = Product.query.filter_by(manufacturing_id = session["user_id"]).all()

    return render_template("products.html" , products=products)


# Route for edit product details 
@app.route("/edit-product/<int:id>", methods=["GET","POST"])
def edit_product(id):

    product = Product.query.get(id)

    if request.method == "POST":

        product.name = request.form.get("name")
        product.description = request.form.get("description")
        product.price = request.form.get("price") or product.price
        product.manufacturing_cost = request.form.get("manufacturing_cost")
        product.delivery_time = request.form.get("delivery_time")

        db.session.commit()

        return redirect("/my-products")

    return render_template("edit_product.html", product=product)



#Route for delete product 
@app.route("/delete-product/<int:id>", methods=["POST"])
def delete_product(id):

    if "user_id" not in session:
        return redirect("/")

    product = Product.query.get_or_404(id)

    if product.manufacturing_id != session["user_id"]:
        return "Unauthorized", 403

    db.session.delete(product)
    db.session.commit()

    return redirect("/my-products")

# Route for logout 
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")




# Route for gen AI description 
@app.route("/generate-description", methods=["POST"])
def ai_description():

    product_name = request.form.get("name")
    category = request.form.get("category")

    if category == "Other":
        category = request.form.get("custom_category")

    description = generate_description(product_name, category)

    formatted_description = markdown.markdown(description)

    return formatted_description





# Route for genAI title 
@app.route("/generate-title", methods=["POST"])
def ai_title():

    product_name = request.form.get("name")
    category = request.form.get("category")

    if not product_name or not category:
        return "Enter product name and category first."

    title = generate_title(product_name, category)

    return title



# Route for Ai Generated seo tags 
@app.route("/generate-keywords", methods=["POST"])
def ai_keywords():

    product_name = request.form.get("name")
    category = request.form.get("category")

    keywords = generate_keywords(product_name, category)

    formatted = markdown.markdown(keywords)

    return formatted



# Route for AI market competitor analysis
@app.route("/market-analysis", methods=["POST"])
def ai_market():

    product_name = request.form.get("name")
    category = request.form.get("category")
    cost = request.form.get("cost")

    result = generate_market_analysis(product_name, category, cost)

    formatted = markdown.markdown(result)

    return formatted



# Route for AI smart final price
@app.route("/generate-final-price", methods=["POST"])
def ai_final_price():

    product_name = request.form.get("name")
    category = request.form.get("category")
    cost = request.form.get("cost")

    result = generate_final_price(product_name, category, cost)

    formatted = markdown.markdown(result)

    return formatted









# CUSTOMER MODULE 


# Route to browse marketplace of customer module 
@app.route("/products")
def marketplace():

    search = request.args.get("search")
    category = request.args.get("category")
    sort = request.args.get("sort")

    query = Product.query

    # PROFESSIONAL SEARCH
    if search:
        query = query.filter(
            or_(
                Product.title.ilike(f"%{search}%"),
                Product.name.ilike(f"%{search}%"),
                Product.category.ilike(f"%{search}%"),
                Product.description.ilike(f"%{search}%")
            )
        )

    # CATEGORY FILTER
    if category:
        query = query.filter(Product.category == category)

    # SORTING
    if sort == "price_low":
        query = query.order_by(Product.price.asc())

    elif sort == "price_high":
        query = query.order_by(Product.price.desc())

    elif sort == "delivery_fast":
        query = query.order_by(Product.delivery_time.asc())

    products = query.all()

    return render_template("marketplace.html", products=products)



# Route for the view details of the product page of customer module
@app.route("/product/<int:id>")
def product_detail(id):

    product = Product.query.get(id)

    reviews = Review.query.filter_by(product_id=id).all()

    return render_template(
        "product_detail.html",
        product=product,
        reviews=reviews
    )




# Route for AI Generated Summary of the description of product in vire product details page of customer module 
@app.route("/ai-summary", methods=["POST"])
def ai_summary():

    title = request.form.get("title")
    description = request.form.get("description")

    result = generate_summary(title, description)

    return markdown.markdown(result)



# Route for User give the ratings and that rating should store in the database in costomer module 
@app.route("/add-review/<int:product_id>", methods=["POST"])
def add_review(product_id):

    if "user_id" not in session:
        return redirect("/")

    rating = request.form.get("rating")
    comment = request.form.get("comment")

    review = Review(
        product_id=product_id,
        user_name=session["name"],
        rating=rating,
        comment=comment
    )

    db.session.add(review)
    db.session.commit()

    return redirect(f"/product/{product_id}")


# Ai Generated review of product by seeing different customer reviews 
@app.route("/ai-review-analysis/<int:product_id>")
def ai_review_analysis(product_id):

    reviews = Review.query.filter_by(product_id=product_id).all()

    review_text = "\n".join([r.comment for r in reviews])

    result = generate_review_insight(review_text)

    return markdown.markdown(result)



# Route to Add to cart 
@app.route("/add-to-cart/<int:product_id>")
def add_to_cart(product_id):

    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]

    cart_item = Cart.query.filter_by(
        user_id=user_id,
        product_id=product_id
    ).first()

    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = Cart(
            user_id=user_id,
            product_id=product_id,
            quantity=1
        )

        db.session.add(cart_item)

    db.session.commit()

    return redirect("/cart")



# Route to Cart page 
@app.route("/cart")
def cart():

    if "user_id" not in session:
        return redirect("/")

    cart_items = Cart.query.filter_by(user_id=session["user_id"]).all()

    total = sum(item.subtotal for item in cart_items)

    return render_template("cart.html", products=cart_items, total=total)



# Route to increate quantity in the cart 
@app.route("/increase-qty/<int:product_id>")
def increase_qty(product_id):

    cart = Cart.query.filter_by(
        user_id=session["user_id"],
        product_id=product_id
    ).first()

    if cart:
        cart.quantity += 1
        db.session.commit()

    return redirect("/cart")



# Route to decrease quantity in cart 
@app.route("/decrease-qty/<int:product_id>")
def decrease_qty(product_id):

    cart = Cart.query.filter_by(
        user_id=session["user_id"],
        product_id=product_id
    ).first()

    if cart and cart.quantity > 1:
        cart.quantity -= 1
        db.session.commit()

    return redirect("/cart")


#Route to remove product from cart 
@app.route("/remove-from-cart/<int:product_id>")
def remove_from_cart(product_id):

    cart = Cart.query.filter_by(
        user_id=session["user_id"],
        product_id=product_id
    ).first()

    if cart:
        db.session.delete(cart)
        db.session.commit()

    return redirect("/cart")



# Route to buy product page 
@app.route("/checkout", methods=["GET","POST"])
def checkout():

    if "user_id" not in session:
        return redirect("/")

    cart_items = Cart.query.filter_by(user_id=session["user_id"]).all()

    total = sum(item.subtotal for item in cart_items)

    if request.method == "POST":

        address = request.form.get("address")
        payment = request.form.get("payment")

        # create order
        new_order = Order(
            user_id=session["user_id"],
            total_price=total,
            address=address,
            payment_method=payment
        )

        db.session.add(new_order)
        db.session.commit()


        # save order items
        for item in cart_items:

            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price
            )

            db.session.add(order_item)

        db.session.commit()


        # clear cart
        for item in cart_items:
            db.session.delete(item)

        db.session.commit()

        return redirect("/order-success")

    return render_template("checkout.html", products=cart_items, total=total)

# Route to Successful order
@app.route("/order-success")
def order_success():

    return render_template("order_success.html")


# Route to my orders 
@app.route("/orders")
def my_orders():
    if "user_id" not in session:
        return redirect("/")
    orders = Order.query.filter_by(user_id=session["user_id"]).order_by(Order.id.desc()).all()
    order_data = []
    for order in orders:
        items = OrderItem.query.filter_by(order_id=order.id).all()
        order_data.append({
            "order": order,
            "order_items": items
        })

    return render_template("orders.html", orders=order_data)


if(__name__) == "__main__":
    app.run(debug = True)