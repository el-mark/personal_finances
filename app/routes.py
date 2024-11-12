from app import app
from flask import render_template, request, redirect, url_for, flash
from app.models import Email, Transaction
from app import db
from openai import OpenAI
import os
from app.services.email_into_transaction import EmailIntoTransaction
import json



client = OpenAI(api_key=os.environ.get('OPENAI_KEY'))

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

        EmailIntoTransaction().call(new_email)

        return redirect(url_for('index'))
    return render_template('email_form.html')

@app.route('/transactions')
def transactions():
    all_transactions = Transaction.query.all()
    return render_template('transactions.html', transactions=all_transactions)

@app.route('/chatgpt')
def chatgpt():
    user_input = """
        transform this transaction email text
        "Constancia de Pago Plin
        10 Nov 2024 11:26 AM
        from: Interbank Servicio al Cliente <servicioalcliente@netinterbank.com.pe>
        Código de operación:	01483653
        Cuenta cargo:	Ahorro Sueldo Soles
        108 3094799772
        Destinatario:	Samuel Antonio Pezua Espinoza
        Destino:	Plin
        Moneda y monto:	S/ 13.20"
        
        into a json object like this:
        {
            fecha: '2024-12-31',
            codigo_de_operacion: 12345,
            banco: 'Interbank',
            cuenta_cargo: 'Juan Perez',
            cuenta_destino: '1234567890',
            moneda: USD,
            monto: 30
        }

        moneda tiene que ser: PEN, USD o NONE

        return only the json object
    """
    # response = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[{"role": "user", "content": user_input}]
    # )

    # message = response.choices[0].message.content
    # print(message)

    message = """```json
        {
            "fecha": "2024-12-31",
            "codigo_de_operacion": "01483653",
            "banco": "Interbank",
            "cuenta_cargo": "Ahorro Sueldo Soles 108 3094799772",
            "cuenta_destino": "Samuel Antonio Pezua Espinoza",
            "moneda": "PEN",
            "monto": 13.20
        }
        ```
    """
    parsed_message = message.replace("```json", "").replace("```", "")

    print(EmailIntoTransaction(user_input).call())

    json_data = json.loads(parsed_message)

    return render_template('chatgpt.html', message=json_data["moneda"])
