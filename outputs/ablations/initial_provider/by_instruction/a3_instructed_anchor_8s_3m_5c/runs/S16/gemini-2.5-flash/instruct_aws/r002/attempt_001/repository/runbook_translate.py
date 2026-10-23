import os
import boto3
from typing import List, Dict, Any
from botocore.exceptions import ClientError
from security_models import AuditNote

class AWSTranslateClient:
    def __init__(self):
        self.client = boto3.client('translate')

    def translate_text(self, text: str, source_language_code: str, target_language_code: str) -> str:
        try:
            response = self.client.translate_text(
                Text=text,
                SourceLanguageCode=source_language_code,
                TargetLanguageCode=target_language_code
            )
            return response.get('TranslatedText')
        except ClientError as e:
            print(f"Error translating text: {e}")
            raise

def translate_runbook_notes(audit_notes: List[AuditNote], target_language: str = 'es') -> Dict[str, str]:
    translate_client = AWSTranslateClient()
    translated_notes = {}
    for note in audit_notes:
        if note.content:
            translated_text = translate_client.translate_text(
                text=note.content,
                source_language_code='en',  # Assuming English as source, can be extended to detect language
                target_language_code=target_language
            )
            translated_notes[note.note_id] = translated_text
    return translated_notes
