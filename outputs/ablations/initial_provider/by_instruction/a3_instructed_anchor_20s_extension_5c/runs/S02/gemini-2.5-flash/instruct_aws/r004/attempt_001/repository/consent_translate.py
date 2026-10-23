import os
import boto3
import json
from typing import Dict, Any

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

def translate_consent_copy(text: str, source_language_code: str, target_language_code: str) -> Dict[str, Any]:
    """
    Translates identity-provider consent copy using AWS Translate.
    """
    client = boto3.client("translate", region_name=AWS_REGION)

    try:
        response = client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )
        return {
            "translated_text": response.get("TranslatedText"),
            "source_language": response.get("SourceLanguageCode"),
            "target_language": response.get("TargetLanguageCode"),
        }
    except client.exceptions.InvalidRequestException as e:
        print(f"Invalid request for Translate: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Error translating consent copy with AWS Translate: {e}")
        raise

if __name__ == "__main__":
    english_consent_copy = "By continuing, you agree to our Terms of Service and Privacy Policy."
    spanish_target_language = "es"
    french_target_language = "fr"

    try:
        spanish_translation = translate_consent_copy(english_consent_copy, "en", spanish_target_language)
        print(f"English: {english_consent_copy}")
        print(f"Spanish Translation: {json.dumps(spanish_translation, indent=2)}")

        print("\n---" )

        french_translation = translate_consent_copy(english_consent_copy, "en", french_target_language)
        print(f"English: {english_consent_copy}")
        print(f"French Translation: {json.dumps(french_translation, indent=2)}")

    except Exception as e:
        print(f"An error occurred: {e}")
