from google.cloud import translate_v2 as translate
from identity_models import TranslateRequest, TranslateResponse
import os

def welcome_translate(request: TranslateRequest) -> TranslateResponse:
    client = translate.Client()
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable for authentication
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"
    
    response = client.translate(request.text, target_language=request.target_language)
    return TranslateResponse(translated_text=response["translatedText"])
