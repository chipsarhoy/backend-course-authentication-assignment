from flask import jsonify, request
from flask_bcrypt import generate_password_hash

from db import db
from lib.authenticate import authenticate_return_auth
from models.app_user import AppUsers, user_schema, users_schema
from util.reflection import populate_object


def create_user():
    post_data = request.form if request.form else request.json

    check_super_admin = db.session.query(AppUsers).filter(AppUsers.role == "super-admin").first()

    if post_data.get("role") == "super-admin" and check_super_admin:
        return jsonify({"message": "super admin account already exists"}), 400

    new_user = AppUsers.new_user_obj()

    populate_object(new_user, post_data)

    new_user.password = generate_password_hash(new_user.password).decode("utf8")

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "user created", "result": user_schema.dump(new_user)}), 201

@authenticate_return_auth
def get_all_users(auth_info):
    if auth_info.user.role == "user":
        return jsonify({"message": "invalid permissions"}), 403

    users = db.session.query(AppUsers).all()

    return jsonify({"message": "users found", "results": users_schema.dump(users)}), 200

@authenticate_return_auth
def update_user_by_id(user_id, auth_info):
    if user_id != str(auth_info.user.user_id) and auth_info.user.role == "user":
        return jsonify({"message": "invalid permissions"}), 403

    put_data = request.form if request.form else request.json

    user = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()
    
    if not user:
        return jsonify({"message": "user does not exist"}), 404

    if user.role == "super-admin" and auth_info.user.role != "super-admin":
        return jsonify({"message": "invalid permissions"}), 403

    populate_object(user, put_data)

    db.session.commit()
    return jsonify({"message": "user updated", "result": user_schema.dump(user)}), 200

@authenticate_return_auth
def delete_user_by_id(user_id, auth_info):
    if user_id != str(auth_info.user.user_id) and auth_info.user.role == "user":
        return jsonify({"message": "invalid permissions"}), 403

    user = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()

    if user.role == "super-admin":
        return jsonify({"message": "invalid permissions"}), 403

    if not user:
        return jsonify({"message": "user does not exist"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "unable to delete user"}), 400
    
    return jsonify({"message": "user deleted"}), 200