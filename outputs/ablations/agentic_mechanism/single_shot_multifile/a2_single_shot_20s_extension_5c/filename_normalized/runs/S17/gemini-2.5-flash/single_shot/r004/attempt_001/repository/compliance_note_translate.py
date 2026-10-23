from security_client import SecurityClientConfig
from security_models import TranslationResult

def translate_compliance_notes(text: str, target_lang: str = "es") -> TranslationResult:
    translate_client = SecurityClientConfig.get_gcp_translate_client()
    project_id = SecurityClientConfig.get_gcp_project_id()

    parent = f"projects/{project_id}"

    response = translate_client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_lang
        }
    )

    translated_text = ""
    source_language = ""
    if response.translations:
        translated_text = response.translations[0].translated_text
        source_language = response.translations[0].detected_language_code
    
    return TranslationResult(
        original_text=text,
        translated_text=translated_text,
        source_language=source_language,
        target_language=target_lang
    )