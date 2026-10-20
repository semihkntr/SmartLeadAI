import requests
import os
import logging
import traceback
from typing import List, Dict, Optional
from config import config_dict

class AIServiceError(Exception):
    pass

class AIService:
    def __init__(self) -> None:
        env = os.environ.get('FLASK_ENV', 'development')
        self.config = config_dict.get(env, config_dict['default'])
        self.api_key = getattr(self.config, 'GROQ_API_KEY', None)
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "openai/gpt-oss-20b"

    def _sistem_talimatini_al(self) -> str:
        context = getattr(self.config, 'BUSINESS_CONTEXT', None)
        if not context:
            return "Sen SeaSoftware asistanısın."
        return context

    def yanit_uret(self, mesaj: str, gecmis: Optional[List[Dict[str, str]]] = None) -> str:
        if gecmis is None:
            gecmis = []

        if not self.api_key or self.api_key == 'anahtar-yok':
            logging.warning("[YAPAY ZEKA] API anahtarı eksik. Demo modu çalışıyor.")
            return "Demo Modu: Merhaba, ben SeaSoft asistanıyım."

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
            
            if response.status_code != 200:
                hata_detayi = response.text
                logging.error(f"[GROQ API REDDEDİLDİ] Status: {response.status_code} - Hata: {hata_detayi}")
                raise Exception(f"Groq API Reddedildi ({response.status_code}): {hata_detayi}")
                
            response.raise_for_status() 
            yanit_verisi = response.json()
            return yanit_verisi['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            logging.error(f"[AĞ HATASI] Yapay Zeka servisine ulaşılamadı.\nDetay: {traceback.format_exc()}")
            raise AIServiceError(f"API isteği başarısız oldu: {str(e)}")
        except KeyError as e:
            logging.error(f"[JSON FORMAT HATASI] Groq'tan beklenmeyen format döndü.\nDetay: {traceback.format_exc()}")
            raise AIServiceError("Yapay zeka yanıt formatı anlaşılamadı.")
        except Exception as e:
            logging.error(f"[YAPAY ZEKA BEKLENMEYEN HATA]\nDetay: {traceback.format_exc()}")
            raise AIServiceError(f"Yapay zeka ile iletişim kurulamadı: {str(e)}")

ai_service = AIService()