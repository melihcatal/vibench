from google.cloud import translate_v3beta1 as translate

def translate_script(text: str, target_language: str, project_id: str) -> str:
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
        mime_type="text/plain",
    )

    return response.translations[0].translated_text
