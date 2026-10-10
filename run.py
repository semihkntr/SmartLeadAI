from app import create_app
import os

# Uygulama fabrikasından app nesnesini al
app = create_app()

if __name__ == '__main__':
    # .env'den port bilgisini al, yoksa 5000'i kullan
    port = int(os.environ.get("PORT", 5000))
    # Sunucuyu başlat
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])