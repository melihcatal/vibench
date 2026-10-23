import os
from typing import Dict, Any
from security_client import get_translate_client

def translate_compliance_note(text: str, source_language_code: str, target_language_code: str, region: str = 'us-east-1') -> str:
    """
    Translates encryption or compliance notes for reviewers using Amazon Translate.
    """
    translate_client = get_translate_client(region)
    
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )
    
    return response['TranslatedText']

if __name__ == '__main__':
    # This is example usage and should not be part of the final submission.
    # Ensure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION are set in environment variables.
    
    # example_note_en = "Encryption key rotation was performed in accordance with compliance policy 2.1.3."
    # example_note_es = "La rotación de la clave de cifrado se realizó de acuerdo con la política de cumplimiento 2.1.3."
    
    # # Translate English to Spanish
    # translated_to_es = translate_compliance_note(example_note_en, "en", "es")
    # print(f"English to Spanish: {translated_to_es}")

    # # Translate Spanish to English
    # translated_to_en = translate_compliance_note(example_note_es, "es", "en")
    # print(f"Spanish to English: {translated_to_en}")
