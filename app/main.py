from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS


from app.config import settings
from app.models import ShowSearchInput, LogInput

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = str(settings.SQLALCHEMY_DATABASE_URI)
CORS(app)

db = SQLAlchemy(app)

app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)


@app.route("/access-token", methods=["POST"])
def login():
    from app.db.crud import authenticate

    try:
        login_data = LogInput.model_validate(request.get_json())

        user = authenticate(
            session=db.session,
            username=login_data.username,
            password=login_data.password,
        )
        if not user:
            return jsonify({"message": "Incorrect email or password"}), 400
        elif not user.is_active:
            return jsonify({"message": "Inactive user"}), 400
        access_token = create_access_token(identity=user.id)
        return jsonify({"message": "Login Success", "access_token": access_token}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/movies", methods=["POST"])
def get_movies():
    from app.db.crud import search_movies

    try:
        input = ShowSearchInput.model_validate(request.get_json())
        filter = input.model_dump(exclude_none=True, exclude={"offset", "limit"})
        limit = input.limit
        offset = input.offset
        movies = search_movies(
            session=db.session, filters=filter, limit=limit, offset=offset
        )
        if not movies:
            return jsonify("No result"), 404
        return jsonify(
            [
                {
                    "show_id": m.show_id,
                    "type": m.type,
                    "title": m.title,
                    "director": m.director,
                    "cast": m.cast,
                    "date_added": m.date_added.strftime("%Y-%m-%d"),
                    "release_year": m.release_year,
                    "rating": m.rating,
                    "duration": m.duration,
                    "description": m.description,
                    "country": m.country,
                    "listed_in": m.listed_in,
                }
                for m in movies
            ]
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health-check", methods=["GET"])
def health_check():
    return jsonify(True)
