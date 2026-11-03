import os

import bcrypt
from database import engine, init_db
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from models import User
from sqlalchemy.orm import Session

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ.get(
    "JWT_SECRET_KEY", "dev-secret-change-in-prod"
)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = int(
    os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", str(3600))
)

jwt = JWTManager(app)

init_db()


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    full_name = data.get("full_name")

    if not all([email, username, password]):
        return jsonify({"error": "Missing required fields"}), 400

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    with Session(engine) as session:
        existing_user = (
            session.query(User)
            .filter((User.username == username) | (User.email == email))
            .first()
        )
        if existing_user:
            return jsonify({"error": "Username or email already exists"}), 400

        new_user = User(
            username=username,
            email=email,
            full_name=full_name,
            hashed_password=hashed_password.decode("utf-8"),
        )
        session.add(new_user)
        session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    with Session(engine) as session:
        user = session.query(User).filter_by(email=email).first()
        if not user or not bcrypt.checkpw(
            password.encode("utf-8"), user.hashed_password.encode("utf-8")
        ):
            return jsonify({"error": "Invalid username or password"}), 401

        access_token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": access_token}), 200


@app.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = int(get_jwt_identity())
    with Session(engine) as session:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        return (
            jsonify(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "full_name": user.full_name,
                }
            ),
            200,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", str(8001))))
