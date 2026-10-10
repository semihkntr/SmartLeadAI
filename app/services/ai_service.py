import requests
import os
from config import config_dict

class AIServiceError(Exception):
    """Yapay zeka servisi hataları için özel hata sınıfı."""
    pass

class AIService:
    def __init__(self):
        # Ortam değişkenine göre doğru config sınıfını alıyoruz
        env = os.environ.get('FLASK_ENV', 'development')
        self.config = config_dict.get(env, config_dict['default'])
        self.api_key = self.config.GROQ_API_KEY
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.1-8b-instant"

    def _sistem_talimatini_al(self):
        """Config'den yapay zeka kişiliğini (BUSINESS_CONTEXT) okur."""
        return self.config.BUSINESS_CONTEXT

    def yanit_uret(self, mesaj, gecmis=None):
        """Kullanıcı mesajını Groq API'sine gönderir ve yanıtı döndürür."""
        if gecmis is None:
            gecmis = []

        # Demo Modu: API anahtarı yoksa çökmek yerine demo mesajı dön.
        if not self.api_key or self.api_key == 'anahtar-yok':
            return "Demo Modu: Merhaba, ben SeaSoft asistanıyım. (API anahtarı girilmediği için otomatik yanıt veriyorum.)"

        # Mesaj dizilimi: Sistem talimatı (system) -> Geçmiş -> Yeni Mesaj (user)
        messages = [{"role": "system", "content": self._sistem_talimatini_al()}]
        
        for g_mesaj in gecmis:
            messages.append(g_mesaj)
            
        messages.append({"role": "user", "content": mesaj})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": messages
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status() # HTTP hatalarını yakalar
            
            yanit_verisi = response.json()
            return yanit_verisi['choices'][0]['message']['content']
            
        except Exception as e:
            # Hataları yakalayıp kibarca fırlatıyoruz
            raise AIServiceError(f"Yapay zeka ile iletişim kurulamadı: {str(e)}")

# Dosyanın sonunda tek bir örnek (instance) oluşturuyoruz
ai_service = AIService()