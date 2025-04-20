from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = '700e4c00bca577bede8fff2e08d359c7f5dfa7f80bd6fe4de2d6d77f54981796'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)

from project import routes

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=9000)