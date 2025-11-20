from flask import Flask
from routes.cases import cases_bp
from routes.donations import donations_bp
from routes.hospitals import hospitals_bp
from routes.admin import admin_bp
from routes.common import common_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'resqtrack_secret_key'
    
    # Register blueprints
    app.register_blueprint(cases_bp)
    app.register_blueprint(donations_bp)
    app.register_blueprint(hospitals_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(common_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)