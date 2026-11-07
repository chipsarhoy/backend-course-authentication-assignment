import uuid
from flask import jsonify, request

from db import db
from lib.authenticate import authenticate, authenticate_return_auth
from models.category import Categories, category_schema, categories_schema
from util.reflection import populate_object

@authenticate_return_auth
def add_category(auth_info):
    if auth_info.user.role not in ["admin", "super-admin"]:
        return jsonify({"message": "invalid permissions"}), 403
    
    post_data = request.form if request.form else request.json

    new_category = Categories.new_category_obj()

    populate_object(new_category, post_data)

    db.session.add(new_category)
    db.session.commit()    

    return jsonify({"messasge": "category created", "results": category_schema.dump(new_category)}), 201

@authenticate
def get_all_categories():
    categories = db.session.query(Categories).all()

    return jsonify({"message": "categories found", "results":  categories_schema.dump(categories)}), 200

@authenticate
def get_category_by_id(category_id):    

    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category_query:
        return jsonify({"message": "category does not exist"}), 404

    return jsonify({"message": "category found", "result": category_schema.dump(category_query)}), 200

@authenticate_return_auth
def update_category_by_id(category_id, auth_info):
    if auth_info.user.role not in ["admin", "super-admin"]:
        return jsonify({"message": "invalid permissions"}), 403
    
    post_data = request.form if request.form else request.json

    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category_query:
        return jsonify({"message": "category does not exist"}), 404

    populate_object(category_query, post_data)    

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "unable to update category"}), 400

    return jsonify({"message": "category updated", "result": category_schema.dump(category_query)})

@authenticate_return_auth
def delete_category_by_id(category_id, auth_info):    
    if auth_info.user.role not in ["admin", "super-admin"]:
        return jsonify({"message": "invalid permissions"}), 403
    
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category_query:
        return jsonify({"message": "category does not exist"}), 404

    try:
        db.session.delete(category_query)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "unable to delete category"}), 400

    return jsonify({"message": "category deleted"}), 200