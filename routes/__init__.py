from .index_route import index_bp
from .form_route import form_bp

def register_routes(app):
    app.register_blueprint(index_bp)
    app.register_blueprint(form_bp)