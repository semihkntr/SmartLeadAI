import logging
import sys
import traceback
import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import config_dict

def create_app():
    app = Flask(__name__)
    CORS(app) 
    
    env = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config_dict.get(env, config_dict['default']))

    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | [%(levelname)s] | %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    
    with app.app_context():
        from app.database import init_db
        init_db(app)
        
    from app.routes import pages_bp, api_bp
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.route('/health')
    def health_check():
        return jsonify({'durum': 'aktif', 'mesaj': 'SeaSoft SmartLead AI çalışıyor!'})

    @app.errorhandler(Exception)
    def handle_exception(e):
        hata_mesaji = f"CRITICAL ERROR (GLOBAL): {str(e)}\nDetay:\n{traceback.format_exc()}"
        app.logger.error(hata_mesaji)
        
        return jsonify({
            "basari": False, 
            "mesaj": "Sunucuda beklenmeyen bir hata oluştu.", 
            "hata_kodu": 500
        }), 500
        
    return app