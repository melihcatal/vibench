import os
from google.cloud import translate_v2 as translate
from identity_models import RegisterResponse

_translate_client = None

def get_translate_client():
    global _translate_client
    if _translate_client is None:
        _translate_client = translate.Client.from_service_account_json(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )
    return _translate_client

def translate_welcome_message(user: RegisterResponse, target_language: str) -> str:
    client = get_translate_client()
    welcome_text = f"Welcome, {user.display_name}! Your account is ready."
    result = client.translate(
        welcome_text,
        target_language=target_language,
        source_language="en"
    )
    return result["translatedText"]