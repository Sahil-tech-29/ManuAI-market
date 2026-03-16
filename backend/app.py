from flask import Flask,render_template,request,session,redirect,Response
from database import db
from models import User
from models import Product
import os
from werkzeug.utils import secure_filename
from ai_utils import generate_description,generate_title,generate_keywords,generate_market_analysis,generate_final_price
import markdown 


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
@app.route("/" ,methods =["GET","POST"])
def home():
    if request.method =="POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email = email , password = password).first()

        if user:
            session["user_id"] = user.id
            session["role"] = user.role
            session["name"] = user.name
            return redirect("/dashboard")
        
        else:
            return Response("Invalid email or password")

    return render_template("index.html")



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
        price = request.form.get("price")
        manufacturing_cost = request.form.get("manufacturing_cost")
        delivery_time = request.form.get("delivery_time")

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




# Route for delete product 
@app.route("/delete-product/<int:id>")
def delete_product(id):

    product = Product.query.get(id)

    db.session.delete(product)
    db.session.commit()

    return redirect("/my-products")




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




if(__name__) == "__main__":
    app.run(debug = True)