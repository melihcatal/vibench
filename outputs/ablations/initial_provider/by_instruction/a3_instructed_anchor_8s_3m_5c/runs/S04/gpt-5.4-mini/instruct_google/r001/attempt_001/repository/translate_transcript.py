from google.cloud import translate_v3


def translate_transcript(text: str, target_language: str = "es"):
    client = translate_v3.TranslationServiceClient()
    response = client.translate_text(
        parent=f"projects/{client.project_path('')}/locations/global",
        contents=[text],
        mime_type="text/plain",
        target_language_code=target_language,
    )
    return response.translations[0].translated_text if response.translations else ""
