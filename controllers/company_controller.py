from flask import jsonify, request

from db import db
from lib.authenticate import authenticate, authenticate_return_auth
from models.company import Companies, company_schema, companies_schema
from util.reflection import populate_object

@authenticate_return_auth
def add_company(auth_info):
    if auth_info.user.role not in ["admin", "super-admin"]:
            return jsonify({"message": "invalid permissions"}), 403
    
    post_data = request.form if request.form else request.json

    new_company = Companies.new_company_obj()

    populate_object(new_company, post_data)

    db.session.add(new_company)
    db.session.commit()    

    return jsonify({"message": "company created", "result": company_schema.dump(new_company)}), 201

@authenticate
def get_all_companies():
    query = db.session.query(Companies).all()    

    return jsonify({"message": "companies found", "results": companies_schema.dump(query)}), 200

@authenticate
def get_company_by_id(company_id):
    query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not query:
        return jsonify({"message": "company does not exist"}), 404

    return jsonify({"message": "company found", "result": company_schema.dump(query)}), 200

@authenticate_return_auth
def update_company_by_id(company_id, auth_info):
    if auth_info.user.role not in ["admin", "super-admin"]:
            return jsonify({"message": "invalid permissions"}), 403
    
    post_data = request.form if request.form else request.json

    query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not query:
        return jsonify({"message": "company does not exist"}), 404

    populate_object(query, post_data)

    db.session.commit()

    return jsonify({"message": "company updated", "result": company_schema.dump(query)}), 200

@authenticate_return_auth
def delete_company_by_id(company_id, auth_info):
    if auth_info.user.role not in ["admin", "super-admin"]:
        return jsonify({"message": "invalid permissions"}), 403
    
    query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not query:
        return jsonify({"message": "company does not exist"}), 404

    try:
        db.session.delete(query)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({'message': "unable to delete record"}), 400

    return jsonify({"message": "company deleted"}), 200