from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token

from app.config import settings


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = str(settings.SQLALCHEMY_DATABASE_URI)


db = SQLAlchemy(app)

app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)


@app.route("/access-token", methods=["POST"])
def login():
    from app.db.crud import authenticate

    data = request.get_json()
    username = data["username"]
    password = data["password"]
    print("Received data:", username, password)

    user = authenticate(session=db.session, username=username, password=password)
    if not user:
        return jsonify({"message": "Incorrect email or password"}), 400
    elif not user.is_active:
        return jsonify({"message": "Inactive user"}), 400
    access_token = create_access_token(identity=user.id)
    return jsonify({"message": "Login Success", "access_token": access_token}), 200


if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True, host="0.0.0.0", port=8000)
