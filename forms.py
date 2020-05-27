from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SearchBar(FlaskForm):
    query = StringField("RecipeGo", render_kw={"placeholder": "search recipes"})
    exclude = StringField("Exclude", render_kw={"placeholder": "exclude ingredients eg: peas"})
    submit = SubmitField("Search")



