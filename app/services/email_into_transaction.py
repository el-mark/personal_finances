import os
from openai import OpenAI
import json

client = OpenAI(api_key=os.environ.get('OPENAI_KEY'))

class EmailIntoTransaction:
    def __init__(self, email_body):
        self.email_body = email_body

    def call(self):
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
                fecha: '31-12-2024',
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
            
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_input}]
        )

        message = response.choices[0].message.content
        print(message)

        json_data = json.loads(message)

        print(json_data)
        print(json_data["fecha"])

        return 'success'

