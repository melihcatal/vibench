from typing import List
from google.cloud import translate
from translation_client import PARENT_LOCATION
from translation_models import normalize_language

def batch_translate(texts: List[str], source_lang: str = "auto", target_lang: str) -> List[str]:
    client = translate.TranslationServiceClient()
    source_code = "" if source_lang.lower() == "auto" else normalize_language(source_lang)
    target_code = normalize_language(target_lang)
    
    response = client.translate_text(
        parent=PARENT_LOCATION,
        contents=texts,
        source_language_code=source_code,
        target_language_code=target_code,
        mime_type="text/plain",
    )
    return [translation.translated_text for translation in response.translations]
