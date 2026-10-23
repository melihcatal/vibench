import requests
from typing import List, Dict, Optional
from pydantic import BaseModel

class TranslationRequest(BaseModel):
    text: List[str]
    target_language: str


class TranslationResponse(BaseModel):
    translations: Optional[List[Dict[str, str]]]
    error: Optional[str]

def translate_transcript(segments: List[str], target_language: str = "es") -> TranslationResponse:
    """
    Translates transcript segments using DeepL API.
    """
    api_key = os.getenv("DEEPL_API_KEY")
    url = "https://api-free.deepl.com/v2/translate"

    payload = {
        "auth_key": api_key,
        "text": segments,
        "target_lang": target_language,
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        result = response.json()
        return TranslationResponse(
            translations=[{"text": t["text"]} for t in result["translations"]],
            error=None
        )
    except Exception as e:
        return TranslationResponse(
            translations=None,
            error=str(e)
        )