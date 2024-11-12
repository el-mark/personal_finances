from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, static_folder='assets')

if __name__ == '__main__':
    app.run(debug=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'your_unique_secret_key'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes
