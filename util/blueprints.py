import routes

def register_blueprint(app):
    app.register_blueprint(routes.auth)
    app.register_blueprint(routes.category)
    app.register_blueprint(routes.company)
    app.register_blueprint(routes.product)
    app.register_blueprint(routes.user)
    app.register_blueprint(routes.warranty)