from typing import Dict, Any, List
from google.cloud import translate
from translation_client import PARENT_LOCATION
from translation_models import normalize_language

def translate_dictionary_values(d: Dict[str, Any], source_lang: str = "auto", target_lang: str) -> Dict[str, Any]:
    client = translate.TranslationServiceClient()
    source_code = "" if source_lang.lower() == "auto" else normalize_language(source_lang)
    target_code = normalize_language(target_lang)
    
    values = [str(v) for v in d.values()]
    response = client.translate_text(
        parent=PARENT_LOCATION,
        contents=values,
        source_language_code=source_code,
        target_language_code=target_code,
        mime_type="text/plain",
    )
    
    translated_values = [t.translated_text for t in response.translations]
    
    return dict(zip(d.keys(), translated_values))
