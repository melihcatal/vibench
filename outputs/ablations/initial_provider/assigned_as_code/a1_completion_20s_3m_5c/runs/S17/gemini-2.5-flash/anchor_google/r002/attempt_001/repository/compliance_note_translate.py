from google.cloud import translate_v3 as translate
from security_models import KeyOperationResult

def translate_compliance_note(text: str, project_id: str, target_language_code: str, source_language_code: str = "en") -> KeyOperationResult:
    client = translate.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
                "source_language_code": source_language_code,
                "target_language_code": target_language_code,
            }
        )

        translated_text = response.translations[0].translated_text
        return KeyOperationResult(success=True, data={"translated_text": translated_text})

    except Exception as e:
        return KeyOperationResult(success=False, error=str(e))
