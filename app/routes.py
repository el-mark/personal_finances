from app import app
from flask import render_template
from app.models import Email

@app.route('/')
def index():
    emails = Email.query.all()
    return render_template('index.html', emails=emails)
