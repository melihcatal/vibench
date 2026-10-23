from google.cloud import translate_v3 as translate
from model_models import ModelOutput


def translate_vertex_ai_output(
    project_id: str,
    text: str,
    target_language_code: str,
    source_language_code: str = "en",
) -> ModelOutput:
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",  # Mime types: "text/plain", "text/html"
        source_language_code=source_language_code,
        target_language_code=target_language_code,
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text

    return ModelOutput(
        text=translated_text, metadata={"target_language": target_language_code}
    )
