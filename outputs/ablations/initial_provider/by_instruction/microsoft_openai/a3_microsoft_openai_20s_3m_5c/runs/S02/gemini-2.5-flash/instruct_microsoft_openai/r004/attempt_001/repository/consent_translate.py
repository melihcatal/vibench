import os
import boto3
from typing import List, Dict, Any

# AWS Translate Configuration
AWS_REGION = os.environ.get("AWS_REGION")

def translate_consent_copy(text: str, source_language_code: str, target_language_code: str) -> Dict[str, Any]:
    """
    Translates identity-provider consent copy using AWS Translate.
    """
    if not AWS_REGION:
        raise ValueError("Missing AWS_REGION environment variable.")

    client = boto3.client('translate', region_name=AWS_REGION)

    try:
        response = client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )
        return {
            "translated_text": response['TranslatedText'],
            "source_language": response['SourceLanguageCode'],
            "target_language": response['TargetLanguageCode'],
            "raw_response": response
        }
    except Exception as e:
        print(f"Error translating text with AWS Translate: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage
    consent_text_en = "By proceeding, you agree to our Terms of Service and Privacy Policy."
    # For a real run, ensure AWS_REGION and credentials are set.
    # translated_text_es = translate_consent_copy(consent_text_en, "en", "es")
    # print(f"English: {consent_text_en}")
    # print(f"Spanish: {translated_text_es.get('translated_text')}")

    # consent_text_fr = "J'accepte les conditions d'utilisation."
    # translated_text_en = translate_consent_copy(consent_text_fr, "fr", "en")
    # print(f"French: {consent_text_fr}")
    # print(f"English: {translated_text_en.get('translated_text')}")
    print("To test, ensure AWS credentials and AWS_REGION are set and call translate_consent_copy.")
