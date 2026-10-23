import os
from typing import List, Dict, Any
from database_client import get_translate_client
from database_models import Document

def translate_document_fields(document: Document, source_lang: str, target_lang: str, fields_to_translate: List[str]) -> Dict[str, Any]:
    translate_client = get_translate_client()
    
    translated_document_data = document.model_dump()

    for field_name in fields_to_translate:
        if hasattr(document, field_name) and isinstance(getattr(document, field_name), str):
            text_to_translate = getattr(document, field_name)
            if text_to_translate:
                try:
                    response = translate_client.translate_text(
                        Text=text_to_translate,
                        SourceLanguageCode=source_lang,
                        TargetLanguageCode=target_lang
                    )
                    translated_document_data[field_name] = response['TranslatedText']
                except translate_client.exceptions.UnsupportedLanguagePairException:
                    translated_document_data[field_name] = f"Error: Unsupported language pair {source_lang}-{target_lang}"
                except Exception:
                    translated_document_data[field_name] = f"Error: Failed to translate {field_name}"

    return translated_document_data
