import os
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri sisteme yükler
load_dotenv()

class Config:
    # Güvenlik ve Veritabanı
    SECRET_KEY = os.environ.get('SECRET_KEY', 'varsayilan-guvenlik-anahtari')
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///leads.db')
    
    # Yapay Zeka Servis Ayarları
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', 'anahtar-yok')
    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'groq')
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
    
    # SeaSoft Markası İçin Yapay Zeka Kişiliği (BUSINESS_CONTEXT)
    BUSINESS_CONTEXT = os.environ.get('BUSINESS_CONTEXT', """Sen SeaSoft markasının yapay zekâ asistanısın. Ziyaretçilere yazılım geliştirme, IT danışmanlık hizmetleri ve marka projeleri hakkında bilgi ver. Profesyonel, yenilikçi ve çözüm odaklı bir dil kullan. Ziyaretçileri ihtiyaçlarına uygun yazılım çözümleri sunmak için iletişim bilgilerini (isim ve telefon) bırakmaya yönlendir.""")

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# Ortama göre (geliştirme veya üretim) doğru sınıfı seçmek için sözlük
config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}