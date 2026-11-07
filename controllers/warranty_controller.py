from flask import jsonify, request

from db import db
from lib.authenticate import authenticate, authenticate_return_auth
from models.warranty import Warranties, warranty_schema
from util.reflection import populate_object

@authenticate_return_auth
def add_warranty(auth_info):
    if auth_info.user.role not in ["admin", "super-admin"]:
            return jsonify({"message": "invalid permissions"}), 403
    
    post_data = request.form if request.form else request.json

    new_warranty = Warranties.new_warranty_obj()

    populate_object(new_warranty, post_data)    

    db.session.add(new_warranty)
    db.session.commit()
    
    return jsonify({"message": "warranty created", "result": warranty_schema.dump(new_warranty)}), 201

@authenticate
def get_warranty_by_id(warranty_id):    
    warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not warranty_query:
        return jsonify({"message": "warranty does not exist"}), 404

    return jsonify({"message": "warranty found", "result": warranty_schema.dump(warranty_query)}), 200

@authenticate_return_auth
def update_warranty_by_id(warranty_id, auth_info):
    if auth_info.user.role not in ["admin", "super-admin"]:
        return jsonify({"message": "invalid permissions"}), 403
    
    post_data = request.form if request.form else request.json

    warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not warranty_query:
        return jsonify({"message": "warranty does not exist"}), 404

    populate_object(warranty_query, post_data)

    db.session.commit()

    return jsonify({"message": "warranty updated", "result": warranty_schema.dump(warranty_query)}), 200

@authenticate_return_auth
def delete_warranty_by_id(warranty_id, auth_info):
    if auth_info.user.role not in ["admin", "super-admin"]:
        return jsonify({"message": "invalid permissions"}), 403
    
    warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not warranty_query:
        return jsonify({"message": "warranty does not exist"}), 404

    try:
        db.session.delete(warranty_query)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "unable to delete warranty"}), 400

    return jsonify({"message": "warranty deleted"}), 200