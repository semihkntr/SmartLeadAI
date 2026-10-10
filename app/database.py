import sqlite3
import os
from flask import g

# Dosyanın bulunduğu klasörü (app) ve bir üst dizini bularak veritabanı yolunu sabitliyoruz
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'leads.db')

def get_db():
    # Veritabanı bağlantısı henüz kurulmadıysa yeni bir tane oluşturur
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        # Sütun adlarıyla verilere erişebilmek için Row factory kullanıyoruz
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db(app):
    # Uygulama bağlamı içinde tabloyu oluşturur
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                email TEXT, 
                mesaj TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Daha önceki denemelerimizde tablo telefonsuz veya emailsiz oluştuysa diye güvenlik yaması
        try:
            db.execute("ALTER TABLE leads ADD COLUMN telefon TEXT DEFAULT '-'")
        except:
            pass
            
        try:
            db.execute("ALTER TABLE leads ADD COLUMN email TEXT DEFAULT '-'")
        except:
            pass
            
        db.commit()

def lead_ekle(isim, telefon, email="", mesaj=""):
    db = get_db()
    db.execute(
        'INSERT INTO leads (isim, telefon, email, mesaj) VALUES (?, ?, ?, ?)',
        (isim, telefon, email, mesaj)
    )
    db.commit()

def tum_leadler():
    # Kayıtları tarihe göre en yeniden eskiye doğru sıralayıp getirir
    db = get_db()
    cursor = db.execute('SELECT * FROM leads ORDER BY tarih DESC')
    return cursor.fetchall()