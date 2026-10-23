import os
from typing import Dict, Any, List
import deepl
from database_models import Document

def translate_document_fields(document: Document, target_lang: str = 'EN', fields: List[str] = None) -> Document:
    if fields is None:
        fields = ['title', 'content', 'description']
    auth_key = os.getenv('DEEPL_AUTH_KEY')
    if not auth_key:
        raise ValueError('DEEPL_AUTH_KEY not set')
    translator = deepl.Translator(auth_key)
    for field in fields:
        if field in document and document[field]:
            result = translator.translate_text(document[field], target_lang=target_lang)
            document[f"{field}_translated"] = result.text
    return document