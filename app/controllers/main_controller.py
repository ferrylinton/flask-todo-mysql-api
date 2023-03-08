from flask import Blueprint, redirect, request, jsonify, url_for, abort
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

blueprint  = Blueprint("main", __name__)
users = {
    'user1': 'user1',
    'user2': 'user2',
    'user3': 'user3',
    'user4': 'user4',
    'user5': 'user5',
}

@blueprint.route("/token", methods=["POST"])
def get_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if username in users and users[username] == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    else:
        return jsonify({"message": "Bad username or password"}), 401
