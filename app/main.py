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


@app.route("/movies", methods=["GET"])
def get_movies():
    from app.db.crud import search_movies

    try:
        title = request.args.get("title")
        director = request.args.get("director")
        release_year = request.args.get("release_year")
        rating = request.args.get("rating")
        limit = int(request.args.get("limit", 10))
        offset = int(request.args.get("offset", 0))

        filters = {}
        if title:
            filters["title"] = title
        if director:
            filters["director"] = director
        if release_year:
            filters["release_year"] = int(release_year)
        if rating:
            filters["rating"] = rating
        movies = search_movies(
            session=db.session, filters=filters, limit=limit, offset=offset
        )
        return jsonify(
            [
                {
                    "show_id": m.show_id,
                    "title": m.title,
                    "director": m.director,
                    "cast": m.cast,
                    "release_year": m.release_year,
                    "rating": m.rating,
                    "duration": m.duration,
                    "description": m.description,
                }
                for m in movies
            ]
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
