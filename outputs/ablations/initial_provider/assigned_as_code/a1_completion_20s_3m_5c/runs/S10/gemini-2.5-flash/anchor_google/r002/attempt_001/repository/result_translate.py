import os
from google.cloud import translate_v2 as translate
from model_models import ModelPayload, ModelResponse

def translate_text_result(payload: ModelPayload) -> ModelResponse:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"
    
    translate_client = translate.Client()
    
    text_to_translate = payload.text
    target_language = payload.target_language or "es" # Default to Spanish if not provided
    
    result = translate_client.translate(text_to_translate, target_language=target_language)
    
    translated_text = result["translatedText"]
    
    return ModelResponse(text=payload.text, translated_text=translated_text)
