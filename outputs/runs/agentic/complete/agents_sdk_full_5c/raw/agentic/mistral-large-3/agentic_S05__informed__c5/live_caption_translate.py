import os
from google.cloud import translate_v3beta1 as translate

def translate_text(text, target_language="es"):
    client = translate.TranslationServiceClient()
    parent = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",
        target_language_code=target_language,
    )

    return response.translations[0].translated_text