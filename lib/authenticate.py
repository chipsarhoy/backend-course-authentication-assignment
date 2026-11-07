from datetime import datetime
from flask import jsonify, request
import functools
from uuid import UUID

from db import db
from models.auth_token import AuthTokens


def validate_uuid4(uuid_string):
    try:
        UUID(uuid_string, version=4)
        return True
    except Exception:
        return False


def validate_token():
    auth_token = request.headers.get("auth")

    if not auth_token or not validate_uuid4(auth_token):
        return False

    existing_token = db.session.query(AuthTokens).filter(AuthTokens.auth_token == auth_token).first()

    if existing_token:
        if existing_token.expiration > datetime.now():
            return existing_token

    return False


def fail_response():
    return jsonify({"message": "authentication required"}), 401


def authenticate(func):
    @functools.wraps(func)
    def wrapper_authenticate(*args, **kwargs):
        auth_info = validate_token()
        return func(*args, **kwargs) if auth_info else fail_response()

    return wrapper_authenticate

def authenticate_return_auth(func):
    @functools.wraps(func)
    def wrapper_authenticate(*args, **kwargs):
        auth_info = validate_token()
        if not auth_info:
            return fail_response()

        kwargs["auth_info"] = auth_info

        return func(*args, **kwargs)
    return wrapper_authenticate