from .endpoints.distributor import distributor


def init_app(app):
    """
    Register app blueprints over here
    eg: # app.register_blueprint(user, url_prefix="/api/users")
    :param app:
    :return:
    """
    app.register_blueprint(distributor, url_prefix="/api/v1/distributors")
