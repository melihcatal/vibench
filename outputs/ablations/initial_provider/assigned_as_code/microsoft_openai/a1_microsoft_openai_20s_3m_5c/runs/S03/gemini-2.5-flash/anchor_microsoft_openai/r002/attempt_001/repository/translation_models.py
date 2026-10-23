from typing import List, Dict, Any
from pydantic import BaseModel, Field

class TranslationRequest(BaseModel):
    text: str
    source_language: str
    target_language: str

class BatchTranslationRequest(BaseModel):
    texts: List[str]
    source_language: str
    target_language: str

class DictionaryTranslationRequest(BaseModel):
    dictionary: Dict[str, str]
    source_language: str
    target_language: str

class TranslationResponse(BaseModel):
    text: str
    source_language: str
    target_language: str

class BatchTranslationResponse(BaseModel):
    translations: List[str]
    source_language: str
    target_language: str

class DictionaryTranslationResponse(BaseModel):
    translated_dictionary: Dict[str, str]
    source_language: str
    target_language: str

# Helper for parsing Azure API response
def parse_azure_translation_response(azure_response: List[Dict[str, Any]]) -> List[str]:
    translated_texts = []
    for item in azure_response:
        if 'translations' in item and item['translations']:
            translated_texts.append(item['translations'][0]['text'])
    return translated_texts
