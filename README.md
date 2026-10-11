# SeaSoft SmartLead AI

## Proje Özeti
**SeaSoft SmartLead AI**, ziyaretçilerle yapay zekâ tabanlı doğal dilde iletişim kuran ve kurumsal iletişim bilgilerini (lead) toplayan uçtan uca bir web sistemidir. Proje, müşteri odaklı bir karşılama sayfası (B2C) ve işletme yöneticilerine özel bir veri paneli (B2B) olmak üzere iki temel arayüzden oluşmaktadır. Sistem, **"Separation of Concerns" (Sorumlulukların Ayrılığı)** prensibine katı bir şekilde bağlı kalınarak modüler bir mimaride geliştirilmiştir.

## Kullanılan Teknolojiler
* **Backend:** Python, Flask
* **Veritabanı:** SQLite
* **Yapay Zekâ Entegrasyonu:** Groq API (llama-3.1-8b-instant)
* **Frontend & Hosting:** Wix Studio (Velo), Render, GitHub

## Mimari Yapı
Sistem kod tabanı tek bir dosyaya yığılmak yerine görevlerine göre izole edilmiştir:

* `config.py`: Tüm çevre değişkenleri ve yapılandırma ayarları tek merkezden yönetilir.
* `database.py`: SQL sorgularını ve veritabanı bağlantılarını barındırır. Kullanıcı verilerinin güvenliği için **SQL Injection** koruması uygulanmıştır.
* `ai_service.py`: Yalnızca Groq API ile iletişim kurar ve hata yönetimini (try-except) sağlar.
* `routes.py`: Gelen HTTP isteklerini (GET/POST) karşılayıp ilgili servislere yönlendirir; içerisinde SQL veya yapay zekâ mantığı barındırmaz.
* `__init__.py` & `run.py`: Uygulama fabrikası ve sunucu başlatma görevlerini üstlenir.



🚀 SeaSoft SmartLead AI

📋 Proje Özeti

SeaSoft SmartLead AI, ziyaretçilerle yapay zekâ tabanlı doğal dilde iletişim kuran ve kurumsal iletişim bilgilerini (lead) toplayan uçtan uca bir web sistemidir. Proje, müşteri odaklı bir karşılama sayfası (B2C) ve işletme yöneticilerine özel bir veri paneli (B2B) olmak üzere iki temel arayüzden oluşmaktadır. Sistem, "Separation of Concerns" (Sorumlulukların Ayrılığı) prensibine katı bir şekilde bağlı kalınarak modüler bir mimaride geliştirilmiştir.

💻 Kullanılan Teknolojiler

Backend: Python, Flask

Veritabanı: SQLite

Yapay Zekâ Entegrasyonu: Groq API (llama-3.1-8b-instant)

Frontend & Hosting: Wix Studio (Velo), Render, GitHub

🏗️ Mimari Yapı

Sistem kod tabanı tek bir dosyaya yığılmak yerine görevlerine göre izole edilmiştir:

config.py: Tüm çevre değişkenleri ve yapılandırma ayarları tek merkezden yönetilir.

database.py: SQL sorgularını ve veritabanı bağlantılarını barındırır. Kullanıcı verilerinin güvenliği için SQL Injection koruması uygulanmıştır.

ai_service.py: Yalnızca Groq API ile iletişim kurar ve hata yönetimini (try-except) sağlar.

routes.py: Gelen HTTP isteklerini (GET/POST) karşılayıp ilgili servislere yönlendirir; içerisinde SQL veya yapay zekâ mantığı barındırmaz.

__init__.py & run.py: Uygulama fabrikası ve sunucu başlatma görevlerini üstlenir.

⚙️ Kurulum ve Çalıştırma

Projeyi yerel ortamda çalıştırmak için aşağıdaki adımları izleyin:

1. Depoyu Klonlayın:

git clone <github-depo-linkiniz>
cd smartlead_ai


2. Sanal Ortamı Kurun ve Aktifleştirin:

python -m venv venv
# Windows için:
venv\Scripts\activate
# macOS/Linux için:
source venv/bin/activate


3. Gereksinimleri Yükleyin:

pip install -r requirements.txt


4. Çevre Değişkenlerini Ayarlayın:
Ana dizinde bir .env dosyası oluşturun ve gizli anahtarlarınızı ekleyin (Bu dosya güvenliğiniz için GitHub'a yüklenmemelidir):

GROQ_API_KEY=gsk_sizin_anahtariniz
SECRET_KEY=gizli_anahtar


5. Uygulamayı Başlatın:

python run.py


Sunucu http://127.0.0.1:5000 adresinde ayağa kalkacaktır. /health uç noktasından sistemin durumunu kontrol edebilir, yerel testlerinizi Postman veya cURL üzerinden /api/sohbet ve /api/leads rotalarıyla gerçekleştirebilirsiniz.
