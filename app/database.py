import sqlite3
import os
import logging
import traceback
from flask import g
from typing import List

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'leads.db')

def get_db() -> sqlite3.Connection:
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db(app) -> None:
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
        try: db.execute("ALTER TABLE leads ADD COLUMN telefon TEXT DEFAULT '-'")
        except Exception: pass
        try: db.execute("ALTER TABLE leads ADD COLUMN email TEXT DEFAULT '-'")
        except Exception: pass
        db.commit()

def lead_ekle(isim: str, telefon: str = "-", email: str = "", mesaj: str = "") -> None:
    try:
        db = get_db()
        db.execute(
            'INSERT INTO leads (isim, telefon, email, mesaj) VALUES (?, ?, ?, ?)',
            (isim, telefon, email, mesaj)
        )
        db.commit()
    except Exception as e:
        logging.error(f"[DB HATASI] lead_ekle fonksiyonu çöktü!\nDetay: {traceback.format_exc()}")
        raise # Hatayı routes.py'a fırlatır ki HTTP 500 döndürebilsin

def tum_leadler() -> List[sqlite3.Row]:
    try:
        db = get_db()
        cursor = db.execute('SELECT * FROM leads ORDER BY tarih DESC')
        return cursor.fetchall()
    except Exception as e:
        logging.error(f"[DB HATASI] tum_leadler fonksiyonu çöktü!\nDetay: {traceback.format_exc()}")
        return []