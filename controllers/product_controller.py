from flask import jsonify, request

from db import db
from lib.authenticate import authenticate, authenticate_return_auth
from models.category import Categories
from models.company import Companies
from models.product import Products, product_schema, products_schema, mini_products_schema
from util.reflection import populate_object

@authenticate_return_auth
def add_product(auth_info):
    if auth_info.user.role not in ["admin", "super-admin"]:
            return jsonify({"message": "invalid permissions"}), 403
    
    post_data = request.form if request.form else request.json

    new_product = Products.new_product_obj()

    populate_object(new_product, post_data)

    db.session.add(new_product)
    db.session.commit()

    return jsonify({"messasge": "product created", "result": product_schema.dump(new_product)}), 201

@authenticate_return_auth
def create_product_category(auth_info):
    if auth_info.user.role not in ["admin", "super-admin"]:
            return jsonify({"message": "invalid permissions"}), 403
    
    post_data = request.form if request.form else request.json
    product_id = post_data.get("product_id")
    category_id = post_data.get("category_id")
    
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if product_query and category_query:
        product_query.categories.append(category_query)
        db.session.commit()

    return jsonify({"message": "category added to product", "result": product_schema.dump(product_query)}), 200

@authenticate
def get_all_products():
    products_query = db.session.query(Products).all()
    
    return jsonify({"message": "products found", "results": products_schema.dump(products_query)}), 200

@authenticate
def get_product_by_id(product_id):

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product_query:
        return jsonify({"message": "product not found"}), 404

    return jsonify({"message": "product found", "result": product_schema.dump(product_query)}), 200

@authenticate    
def get_active_products():

    product_query = db.session.query(Products).filter(Products.active == True).all()       

    return jsonify({"message": "products found", "results": products_schema.dump(product_query)}), 200

@authenticate
def get_products_by_company_id(company_id):

    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company_query:
        return jsonify({"message": "company does not exist"}), 404

    product_query = db.session.query(Products).filter(Products.company_id == company_id).all()    

    return jsonify({"message": "products found", "results": mini_products_schema.dump(product_query)}), 200

@authenticate_return_auth
def update_product_by_id(product_id, auth_info):
    if auth_info.user.role not in ["admin", "super-admin"]:
            return jsonify({"message": "invalid permissions"}), 403
    
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()    
    post_data = request.form if request.form else request.json

    if product_query:
        populate_object(product_query, post_data)

        db.session.commit()
        return jsonify({"message": "product updated", "result": product_schema.dump(product_query)}), 200
    
    return jsonify({"message": "product not found"}), 404

@authenticate_return_auth
def delete_product_by_id(product_id, auth_info):    
    if auth_info not in ["admin", "super-admin"]:
        return jsonify({"message": "invalid permissions"}), 403

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product_query:
        return jsonify({"message": "product does not exist"}), 404

    try:
        db.session.delete(product_query)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"{e}: unable to delete product"}), 400

    return jsonify({"message": "product deleted"}), 200
        