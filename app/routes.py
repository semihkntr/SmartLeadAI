from flask import Blueprint, render_template, request, jsonify
from app.database import lead_ekle, tum_leadler
from app.services.ai_service import ai_service, AIServiceError

pages_bp = Blueprint('pages', __name__)
api_bp = Blueprint('api', __name__)

# --- SAYFA ROTALARI ---

@pages_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@pages_bp.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

# --- API ROTALARI ---

@api_bp.route('/sohbet', methods=['POST'])
def sohbet():
    veri = request.get_json()
    
    if not veri or 'mesaj' not in veri:
        return jsonify({'basari': False, 'hata': 'Mesaj alanı zorunludur.'}), 400

    mesaj = veri['mesaj']
    gecmis = veri.get('gecmis', [])

    try:
        yanit = ai_service.yanit_uret(mesaj, gecmis)
        return jsonify({'basari': True, 'cevap': yanit}), 200
    except AIServiceError as e:
        print(f"Yapay Zeka Hatasi Detayi: {str(e)}")
        return jsonify({'basari': False, 'hata': 'Şu anda asistan hizmet veremiyor, lütfen daha sonra tekrar deneyin.'}), 503

@api_bp.route('/leads', methods=['POST'])
def yeni_lead():
    veri = request.get_json()

    # Yönergeye uygun olarak isim ve telefon ZORUNLU
    if not veri or 'isim' not in veri or 'telefon' not in veri:
        return jsonify({'basari': False, 'hata': 'İsim ve telefon alanları zorunludur.'}), 400

    isim = veri['isim']
    telefon = veri['telefon'] 
    email = veri.get('email', '') # Email ekstra alan olarak ekleniyor
    mesaj = veri.get('mesaj', '')

    try:
        # database.py 4 parametre alacak
        lead_ekle(isim, telefon, email, mesaj)
        return jsonify({'basari': True, 'mesaj': 'Kaydınız başarıyla alındı.'}), 201
    except Exception as e:
        return jsonify({'basari': False, 'hata': 'Kayıt sırasında bir hata oluştu.'}), 500

@api_bp.route('/leads', methods=['GET'])
def leadleri_getir():
    try:
        kayitlar = tum_leadler()
        liste = [dict(kayit) for kayit in kayitlar]
        return jsonify({'basari': True, 'leads': liste}), 200
    except Exception as e:
        return jsonify({'basari': False, 'hata': 'Veriler alınamadı.'}), 500