from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "1234567"  # replace with something random/secure
app.config['TEMPLATES_AUTO_RELOAD'] = True  # auto reload templates

# 'mysql+pymysql://root:your_password@localhost/your_database'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:spnp66mysql@localhost/vendordb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class vendors(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    company = db.Column(db.String(100))
    address = db.Column(db.String(300))
    phone = db.Column(db.Integer)
    email = db.Column(db.String(100))

    def __init__(self, name, company, address, phone, email):
        self.name = name
        self.company = company
        self.address = address
        self.phone = phone
        self.email = email

# ===== Routes =====
# @app.route("/")
# def index():
#     return render_template("index.html")

@app.route("/", methods=["GET", "POST"]) 
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        company = request.form.get("company", "").strip()
        address = request.form.get("address", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        
        new_vendor = vendors(
            name=name,
            company=company,
            address=address,
            phone=phone,
            email=email
        )

        db.session.add(new_vendor)
        db.session.commit()

    # GET request
    flash("welcome to the page. Add correct data", "info")
    return render_template("index.html", form={})

@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    with app.app_context():     # <--- this ensures Flask knows which app to use
        db.create_all()
    app.run(debug=True)

