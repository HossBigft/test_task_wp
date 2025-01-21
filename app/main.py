from sqlalchemy import create_engine

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required


from app.config import settings

app = Flask(__name__)


db = SQLAlchemy(app)

# JWT Initialization
jwt = JWTManager(app)
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)