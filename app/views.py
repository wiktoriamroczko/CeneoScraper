from app import app 
import requests
from flask import render_template, request, redirect, url_for
from flaskext.markdown import Markdown
from app.models import Opinion, Product
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
        page_respons = requests.get("https://www.ceneo.pl/"+product_id)
        if page_respons.status_code == requests.codes['ok']:
            product = Product(product_id)
            product.extract_product()
            product.save_product()
            return redirect(url_for("product", id=product_id))
        else:
            form.product_id.errors.append("Podana wartość nie jest poprawnym kodem produktu.")
    return render_template("extract.html", form=form)

@app.route('/product/<id>')
def product(id):
    pass

@app.route('/products')
def products():
    pass