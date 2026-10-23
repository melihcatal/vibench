import boto3
import os
from security_client import get_translate_client

def translate_compliance_note(text: str, source_language: str, target_language: str) -> str:
    """
    Translates an encryption or compliance note using Amazon Translate.
    """
    translate_client = get_translate_client()
    
    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language
        )
        return response['TranslatedText']
    except Exception as e:
        print(f"Error translating compliance note with Amazon Translate: {e}")
        raise

if __name__ == '__main__':
    # Example Usage
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION_NAME must be set.
    
    english_note = "This data is encrypted at rest using AES-256 and stored in a FIPS 140-2 compliant module."
    
    print("Translating English note to Spanish:")
    try:
        spanish_translation = translate_compliance_note(english_note, 'en', 'es')
        print(f"Spanish: {spanish_translation}")
    except Exception as e:
        print(f"Translation to Spanish failed: {e}")

    print("\nTranslating English note to German:")
    try:
        german_translation = translate_compliance_note(english_note, 'en', 'de')
        print(f"German: {german_translation}")
    except Exception as e:
        print(f"Translation to German failed: {e}")

    french_note = "Ces données sont chiffrées au repos à l'aide de AES-256 et stockées dans un module conforme FIPS 140-2."
    print("\nTranslating French note to English:")
    try:
        english_translation_from_french = translate_compliance_note(french_note, 'fr', 'en')
        print(f"English: {english_translation_from_french}")
    except Exception as e:
        print(f"Translation from French failed: {e}")
