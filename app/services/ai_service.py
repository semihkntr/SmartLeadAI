import requests
import os
from config import config_dict

class AIServiceError(Exception):
    """Yapay zeka servisi hataları için özel hata sınıfı."""
    pass

class AIService:
    def __init__(self):
        env = os.environ.get('FLASK_ENV', 'development')
        self.config = config_dict.get(env, config_dict['default'])
        self.api_key = self.config.GROQ_API_KEY
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama3-8b-8192"

    def _sistem_talimatini_al(self):
        """Config'den yapay zeka kişiliğini okur. Render'da boşsa çökmeyi önlemek için varsayılan metin atar."""
        context = getattr(self.config, 'BUSINESS_CONTEXT', None)
        if not context:
            return "Sen SeaSoftware için çalışan yardımsever, profesyonel bir asistansın ve Türkçe konuşuyorsun."
        return context

    def yanit_uret(self, mesaj, gecmis=None):
        if gecmis is None:
            gecmis = []

        if not self.api_key or self.api_key == 'anahtar-yok':
            return "Demo Modu: Merhaba, ben SeaSoft asistanıyım."

        # Sistem mesajının içeriği kesinlikle string olmalı, boş olursa 400 hatası verir
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
            
            # Eğer 200 Başarılı dışında bir yanıt gelirse (örn: 400 Bad Request), asıl sebebi yakala
            if response.status_code != 200:
                raise Exception(f"Groq API Reddedildi ({response.status_code}): {response.text}")
                
            response.raise_for_status() 
            
            yanit_verisi = response.json()
            return yanit_verisi['choices'][0]['message']['content']
            
        except Exception as e:
            raise AIServiceError(f"Yapay zeka ile iletişim kurulamadı: {str(e)}")

ai_service = AIService()