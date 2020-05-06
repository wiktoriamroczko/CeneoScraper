from app import app 
from flask import render_template, request, redirect, url_for
from flaskext.markdown import Markdown
from app.forms import ProductForm
Markdown(app)

app.config['SECRET_KEY'] = "TajemniczyMysiSprzęt"

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    content = ""
    with open("README.md", "r", encoding="UTF-8") as f:
        content = f.read()
    return render_template("about.html", text=content)

@app.route('/extract', method=['POST', 'GET'])
def extract():
    form = ProductForm()
    if form.validate_on_submit():
        product_id = form.product_id.data
        
        return redirect(url_for("product", id=product_id))
    return render_template("extract.html", form=form)

@app.route('/product/<int:id>')
def product(id):
    pass

@app.route('/products')
def products():
    pass