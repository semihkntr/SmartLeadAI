import logging
import traceback
from flask import Blueprint, request, jsonify, render_template
from app.database import lead_ekle, tum_leadler
from app.services.ai_service import ai_service, AIServiceError

pages_bp = Blueprint('pages', __name__)
api_bp = Blueprint('api', __name__)

@pages_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """Yönetim panelini render eder."""
    return render_template('dashboard.html')

@api_bp.route('/chat', methods=['POST'])
def chat():
    """Kullanıcıdan gelen mesajı Groq AI servisine iletir ve yanıtı döndürür."""
    try:
        data = request.get_json()
        if not data or 'mesaj' not in data:
            logging.warning("[HTTP 400] /api/chat - Eksik parametre: 'mesaj'")
            return jsonify({"basari": False, "mesaj": "Eksik parametre: 'mesaj' zorunludur."}), 400
        
        kullanici_mesaji = data.get('mesaj')
        gecmis = data.get('gecmis', [])
        
        yanit = ai_service.yanit_uret(kullanici_mesaji, gecmis)
        return jsonify({"basari": True, "yanit": yanit}), 200

    except AIServiceError as e:
        logging.error(f"[HTTP 502] /api/chat - AI Servis Hatası: {str(e)}")
        return jsonify({"basari": False, "mesaj": str(e)}), 502
    except Exception as e:
        logging.error(f"[HTTP 500] /api/chat - Sunucu Çökmesi!\nDetay: {traceback.format_exc()}")
        return jsonify({"basari": False, "mesaj": "Yapay zeka ile iletişim sırasında sunucu hatası oluştu."}), 500

@api_bp.route('/leads', methods=['GET'])
@api_bp.route('/adaylar', methods=['GET'])
def get_leads():
    """Dashboard tablosu için veritabanındaki tüm lead'leri hem /leads hem de /adaylar adresinden gönderir."""
    try:
        kayitlar = tum_leadler()
        lead_listesi = [
            {"id": r["id"], "isim": r["isim"], "telefon": r["telefon"], "email": r["email"], "mesaj": r["mesaj"], "tarih": r["tarih"]} 
            for r in kayitlar
        ]
        # Wix Velo kodunun sorunsuz okuyabilmesi için hem 'leads' hem de 'adaylar' anahtarını döndürüyoruz
        return jsonify({"basari": True, "leads": lead_listesi, "adaylar": lead_listesi}), 200
    except Exception as e:
        logging.error(f"[HTTP 500] /api/leads & /adaylar (GET) - Veritabanı Çekme Hatası!\nDetay: {traceback.format_exc()}")
        return jsonify({"basari": False, "mesaj": "Veriler çekilirken hata oluştu."}), 500

@api_bp.route('/leads', methods=['POST'])
@api_bp.route('/adaylar', methods=['POST'])
def create_lead():
    """SeaSoft AI botundan veya Velo'dan gelen yeni müşteri (lead) taleplerini kaydeder."""
    try:
        data = request.get_json()
        if not data or 'isim' not in data:
            logging.warning("[HTTP 400] /api/leads (POST) - Eksik parametre: 'isim'")
            return jsonify({"basari": False, "mesaj": "Eksik parametre: 'isim' zorunludur."}), 400
        
        isim = data.get('isim')
        telefon = data.get('telefon', '-')
        email = data.get('email', '-')
        mesaj = data.get('mesaj', '-')
        
        lead_ekle(isim, telefon, email, mesaj)
        logging.info(f"[BAŞARILI] Yeni Lead Eklendi: {isim}")
        return jsonify({"basari": True, "mesaj": "Kayıt başarıyla oluşturuldu."}), 201

    except Exception as e:
        logging.error(f"[HTTP 500] /api/leads (POST) - Kayıt Eklenirken Hata!\nDetay: {traceback.format_exc()}")
        return jsonify({"basari": False, "mesaj": "Kayıt eklenirken sunucu hatası oluştu."}), 500