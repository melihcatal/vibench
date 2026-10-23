import os
from database_client import get_translate_client
from database_models import Document

def translate_record_field(document: Document, field_to_translate: str, target_language_code: str, source_language_code: str = "auto", region_name: str = None):
    region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
    translate_client = get_translate_client(region_name=region_name)

    text_to_translate = document.get(field_to_translate, "")
    if not text_to_translate:
        return {"translated_field": "", "source_language": ""}

    try:
        response = translate_client.translate_text(
            Text=text_to_translate,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )
        translated_text = response.get("TranslatedText", "")
        actual_source_language = response.get("SourceLanguageCode", source_language_code)
        
        return {"translated_field": translated_text, "source_language": actual_source_language}
    except Exception as e:
        print(f"Translation failed: {e}")
        return {"translated_field": text_to_translate, "source_language": source_language_code, "error": str(e)}
