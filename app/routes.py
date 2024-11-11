from app import app
from flask import render_template, request, redirect, url_for, flash
from app.models import Email
from app import db 


@app.route('/')
def index():
    emails = Email.query.all()
    return render_template('index.html', emails=emails)

@app.route('/email_form', methods=['GET', 'POST'])
def email_form():
    if request.method == 'POST':
        body = request.form['body']
        new_email = Email(body=body)
        db.session.add(new_email)
        db.session.commit()
        flash('Email submitted successfully!')
        return redirect(url_for('index'))
    return render_template('email_form.html')
