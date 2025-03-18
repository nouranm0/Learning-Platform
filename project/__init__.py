from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '700e4c00bca577bede8fff2e08d359c7f5dfa7f80bd6fe4de2d6d77f54981796'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db" 

db = SQLAlchemy(app)


from project import routes