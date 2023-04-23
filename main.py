import os
from flask import Flask, abort, flash, redirect, render_template, url_for
from flask_bootstrap import Bootstrap
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("E-Mail", validators=[DataRequired(), Email()])
    phone_number = StringField("Phone Number", validators=[DataRequired()])
    message = StringField("Message", validators=[DataRequired()])
    submit = SubmitField("Send")


app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET', None)
Bootstrap(app)


@app.route('/', methods=['GET','POST'])
def get_all_posts():
    form = ContactForm()
    if form.validate_on_submit():
        message = Mail(
            from_email=os.getenv('EMAIL'),
            to_emails=os.getenv('EMAIL'),
            subject='New Message',
            html_content=f'Name: {form.name.data} | Email: {form.email.data} | Phone: {form.phone_number.data} | Message: «{form.message.data}»'
        )
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)            
        return render_template("index.html", msg_sent=True, form=form)
    return render_template("index.html", msg_sent=False, form=form)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
