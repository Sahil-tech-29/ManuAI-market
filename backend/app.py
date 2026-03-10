from flask import Flask,render_template,request,session,redirect
from database import db
from models import User



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///manuai.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

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



if(__name__) == "__main__":
    app.run(debug = True)