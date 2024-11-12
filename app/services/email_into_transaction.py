import os
from openai import OpenAI
import json
from app import db
from app.models import Transaction
from datetime import datetime


client = OpenAI(api_key=os.environ.get('OPENAI_KEY'))

class EmailIntoTransaction:
    def call(self, email):
        #       "Constancia de Pago Plin
        # 10 Nov 2024 11:26 AM
        # from: Interbank Servicio al Cliente <servicioalcliente@netinterbank.com.pe>
        # Código de operación:	01483653
        # Cuenta cargo:	Ahorro Sueldo Soles
        # 108 3094799772
        # Destinatario:	Samuel Antonio Pezua Espinoza
        # Destino:	Plin
        # Moneda y monto:	S/ 13.20"

        prompt = f"""
            transform this transaction email text
            {email.body}
            
            into a json object like this:
            {{
                fecha: '2024-12-31',
                codigo_de_operacion: 12345,
                banco: 'Interbank',
                cuenta_cargo: 'Juan Perez',
                cuenta_destino: '1234567890',
                moneda: USD,
                monto: 30
            }}

            moneda tiene que ser: PEN, USD o NONE

            return only the json object
        """
            
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        message = response.choices[0].message.content
        print(message)

        # message = """```json
        #     {
        #         "fecha": "2024-10-13",
        #         "codigo_de_operacion": "01483653",
        #         "banco": "Interbank",
        #         "cuenta_cargo": "Ahorro Sueldo Soles 108 3094799772",
        #         "cuenta_destino": "Samuel Antonio Pezua Espinoza",
        #         "moneda": "PEN",
        #         "monto": 13.20
        #     }
        #     ```
        # """


        parsed_message = message.replace("```json", "").replace("```", "")

        json_data = json.loads(parsed_message)

        transaction = Transaction(
            email_id=email.id,
            transaction_date=datetime.strptime(json_data["fecha"], '%Y-%m-%d').date(),
            transaction_code=json_data["codigo_de_operacion"],
            issuer=json_data["banco"],
            source=json_data["cuenta_cargo"],
            destination=json_data["cuenta_destino"],
            currency=json_data["moneda"],
            amount=json_data["monto"]
        )
        # transaction = Transaction(
        #     email_id=1,
        #     transaction_date=datetime.strptime('2023-01-01', '%Y-%m-%d').date(),
        #     transaction_code='asdf',
        #     issuer='asdf',
        #     source='asdf',
        #     destination='asdf',
        #     currency='asdf',
        #     amount='asdf',
        # )
        db.session.add(transaction)
        db.session.commit()

        return 'success'

