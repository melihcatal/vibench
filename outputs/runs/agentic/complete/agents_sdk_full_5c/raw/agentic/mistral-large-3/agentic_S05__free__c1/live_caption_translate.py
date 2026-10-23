from google.cloud import translate_v3 as translate
import os

def translate_live_captions(text, target_language="es"):
    client = translate.TranslationServiceClient()
    parent = os.getenv("GOOGLE_TRANSLATE_PARENT", f"projects/{\n        os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/global"
    )
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )
    return response.translations[0].translated_text