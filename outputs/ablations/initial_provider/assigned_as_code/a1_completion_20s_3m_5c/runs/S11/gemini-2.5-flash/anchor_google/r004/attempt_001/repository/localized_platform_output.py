from google.cloud import translate
from model_models import ModelResponse

def localized_platform_output(model_response: ModelResponse, target_language: str = "es"):
    client = translate.TranslationServiceClient()

    project_id = model_response.metadata.get("project_id")
    if not project_id:
        raise ValueError("Project ID not found in model response metadata.")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [model_response.text],
            "mime_type": "text/plain",  # Mime types: text/plain, text/html
            "target_language_code": target_language,
        }
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text

    return {"original_text": model_response.text, "translated_text": translated_text, "target_language": target_language}
