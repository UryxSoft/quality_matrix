from flask import Flask
from models import db
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'matriz_indicadores.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'clave_secreta_asd'
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    # Importar y registrar rutas
    from routes import register_routes
    register_routes(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)