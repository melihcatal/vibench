from security_client import SecurityClients
from typing import List, Dict

class TranslationResult:
    def __init__(self, original_text: str, translated_text: str, source_language: str, target_language: str):
        self.original_text = original_text
        self.translated_text = translated_text
        self.source_language = source_language
        self.target_language = target_language

def translate_compliance_notes(
    notes: List[str],
    target_language: str,
    source_language: str = None
) -> List[TranslationResult]:
    translate_client = SecurityClients.get_gcp_translate_client()
    
    translations = []
    for note in notes:
        result = translate_client.translate(
            note,
            target_language=target_language,
            source_language=source_language
        )
        
        translations.append(TranslationResult(
            original_text=note,
            translated_text=result['translatedText'],
            source_language=result.get('detectedSourceLanguage', source_language), # Use detected if source_language wasn't provided
            target_language=target_language
        ))
        
    return translations