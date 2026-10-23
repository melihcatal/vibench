from deep_translator import GoogleTranslator
from identity_client import get_user_locale
from pydantic import BaseModel


class TranslateRequest(BaseModel):
    user_id: str
    text: str


class TranslateResponse(BaseModel):
    translated_text: str


def translate_welcome_message(request: TranslateRequest) -> TranslateResponse:
    locale = get_user_locale(request.user_id)
    if not locale:
        raise ValueError("User locale not found")
    
    translator = GoogleTranslator(source='auto', target=locale)
    translated_text = translator.translate(request.text)
    
    return TranslateResponse(translated_text=translated_text)