from flask import Flask, render_template, url_for, request, redirect, flash
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required, Email

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'
class NameForm(Form):
    mail = StringField('Email-id', validators=[Required(), Email()])
    pwd = PasswordField('Enter Password',validators=[Required()] )
    remember_me = BooleanField('Keep me logged in')
    submitbtn = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    first_last = None
    mail = None
    form = NameForm()
    if form.validate_on_submit():
        first_last = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug = True)

{% extends "bootstrap/base.html" %}
{% import "bootstrap/wtf.html" as wtf %}
{% block title %} LOGIN  {% endblock %}
{% block body %}
{{ super() }}
<form>
    <fieldset>
        <div>
            <h1>LOGIN</h1>
        </div>
        <div>
            {{ wtf.quick_form(form) }}
        </div>
    </fieldset>
</form>
{% endblock %}