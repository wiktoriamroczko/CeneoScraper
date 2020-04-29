from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequaired, Length, Regexp

class ProductForm(FlaskForm):
    product_id = StringField(
        "Podaj kod produktu z serwisu Ceneo.pl: ",
        validators=[
            DataRequaired("Musisz podać kod produktu!"),
            Length(min=6, max=8, message="Kod produktu musi mieć 8 znaków!"),
            Regexp("^[0-9]{8}$", message="Kod produktu może zawierać tylko cyfry!")
        ]
    )
    submit = SubmitField("Pobierz")