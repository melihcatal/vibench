import os
from google.cloud import translate_v2 as translate
from database_models import DocumentResponse, Document


def translate_record_fields(
    document: Document, target_language: str = "es"
) -> DocumentResponse:
    client = translate.Client(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))

    translated_fields = {}
    for key, value in document.content.items():
        if isinstance(value, str):
            try:
                result = client.translate(value, target_language=target_language)
                translated_fields[key] = result["translatedText"]
            except Exception as e:
                translated_fields[key] = f"Translation failed: {e}"
        else:
            translated_fields[key] = value  # Keep non-string fields as is

    document.content["translated_content"] = translated_fields
    return DocumentResponse(
        document=document,
        message=f"Document fields translated to {target_language} successfully.",
    )
