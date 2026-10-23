from typing import List, Dict, Any

# Define common types for translation tasks
# In a more complex scenario, these could be dataclasses or Pydantic models

TranslationText = str
SourceLanguage = str
TargetLanguage = str

class TranslationRequest:
    text: TranslationText
    target_language: TargetLanguage
    source_language: SourceLanguage = None

class TranslationResponse:
    translated_text: TranslationText
    detected_source_language: SourceLanguage = None

class BatchTranslationRequest:
    texts: List[TranslationText]
    target_language: TargetLanguage
    source_language: SourceLanguage = None

class BatchTranslationResponse:
    translated_texts: List[TranslationText]

class DictionaryTranslationRequest:
    dictionary: Dict[str, TranslationText]
    target_language: TargetLanguage
    source_language: SourceLanguage = None

class DictionaryTranslationResponse:
    translated_dictionary: Dict[str, TranslationText]
