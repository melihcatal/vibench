from observability_client import ObservabilityClient
from observability_models import TranslateRequest

def translate_log_message(project_id: str, text_content: str, target_language: str, source_language: str = None):
    client = ObservabilityClient(project_id=project_id)

    translated_texts = client.translate_text(
        text=text_content,
        target_language=target_language,
        source_language=source_language
    )
    
    return {"original_text": text_content, "translated_text": translated_texts[0] if translated_texts else "", "target_language": target_language}
