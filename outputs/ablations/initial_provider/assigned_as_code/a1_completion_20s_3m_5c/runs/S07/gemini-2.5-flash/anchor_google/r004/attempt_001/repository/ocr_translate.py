from google.cloud import translate_v3 as translate

def ocr_translate(text: str, target_language: str, project_id: str) -> str:
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    # The translated text is in the first translation in the response
    return response.translations[0].translated_text
