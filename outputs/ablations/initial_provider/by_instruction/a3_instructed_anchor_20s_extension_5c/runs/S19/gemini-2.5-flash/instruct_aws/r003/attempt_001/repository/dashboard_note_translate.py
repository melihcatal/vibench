import boto3
from typing import Dict, Any

class DashboardNoteTranslator:
    def __init__(self):
        self.translate_client = boto3.client('translate')

    def translate_note(self, text: str, source_language_code: str, target_language_code: str) -> Dict[str, Any]:
        response = self.translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )
        return {
            "original_text": text,
            "translated_text": response.get('TranslatedText'),
            "source_language": response.get('SourceLanguageCode'),
            "target_language": response.get('TargetLanguageCode')
        }
