import os
from google.cloud import translate_v3 as translate
from observability_client import get_translate_client
from observability_models import TranslationRequest

def translate_log_message(translation_request: TranslationRequest) -> str:
    """
    Translates support-visible log messages for another locale using Google Cloud Translation API.
    """
    client = get_translate_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set for Translation API.")

    location = "global" # Or specific region, e.g., "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [translation_request.text_content],
            "target_language_code": translation_request.target_language_code,
            "source_language_code": translation_request.source_language_code,
        }
    )

    translated_text = []
    for translation in response.translations:
        translated_text.append(translation.translated_text)
    
    return " ".join(translated_text)

if __name__ == "__main__":
    # Ensure GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT are set
    # Example log messages
    log_message_en = "User authentication failed due to invalid password."
    log_message_es = "Error al conectar con la base de datos: tiempo de espera agotado."
    log_message_fr = "Tentative de connexion non autorisée détectée."

    print("--- Translating English to Spanish ---")
    req_en_es = TranslationRequest(
        text_content=log_message_en,
        target_language_code="es",
        source_language_code="en"
    )
    translated_es = translate_log_message(req_en_es)
    print(f"Original (en): {log_message_en}")
    print(f"Translated (es): {translated_es}")

    print("\n--- Translating Spanish to English ---")
    req_es_en = TranslationRequest(
        text_content=log_message_es,
        target_language_code="en",
        source_language_code="es"
    )
    translated_en = translate_log_message(req_es_en)
    print(f"Original (es): {log_message_es}")
    print(f"Translated (en): {translated_en}")

    print("\n--- Translating French to German (auto-detect source) ---")
    req_fr_de = TranslationRequest(
        text_content=log_message_fr,
        target_language_code="de"
    )
    translated_de = translate_log_message(req_fr_de)
    print(f"Original (fr): {log_message_fr}")
    print(f"Translated (de): {translated_de}")
