from flask import Flask, jsonify
from flask_cors import CORS # CORS eklendi
from config import config_dict
import os

def create_app():
    app = Flask(__name__)
    
    # CORS'u tüm rotalar için etkinleştir
    CORS(app) 
    
    env = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config_dict.get(env, config_dict['default']))
    
    with app.app_context():
        from app.database import init_db
        init_db(app)
        
    from app.routes import pages_bp, api_bp
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.route('/health')
    def health_check():
        return jsonify({'durum': 'aktif', 'mesaj': 'SeaSoft SmartLead AI çalışıyor!'})
        
    return app