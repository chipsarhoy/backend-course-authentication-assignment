from flask import Blueprint

import controllers

auth = Blueprint("auth", __name__)

@auth.route("/user/auth", methods=["POST"])
def auth_token_add():
    return controllers.auth_token_add()