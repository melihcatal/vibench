import os
from google.cloud import translate_v2 as translate
from typing import List, Dict, Any

def translate_consent_copy(
    text_list: List[str],
    target_language: str,
    source_language: Optional[str] = None
) -> List[Dict[str, Any]]:
    
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # pointing to your service account key file.
    try:
        client = translate.Client()
    except Exception as e:
        print(f"Error initializing Google Cloud Translation client: {e}. Ensure GOOGLE_APPLICATION_CREDENTIALS is set.")
        return [{'error': str(e)} for _ in text_list]

    translations = []
    for text in text_list:
        try:
            if source_language:
                result = client.translate(text, target_language=target_language, source_language=source_language)
            else:
                result = client.translate(text, target_language=target_language)
            translations.append({
                "input": text,
                "translated_text": result['translatedText'],
                "detected_source_language": result['detectedSourceLanguage']
            })
        except Exception as e:
            print(f"Error translating text '{text}': {e}")
            translations.append({"input": text, "error": str(e)})
    
    return translations

if __name__ == "__main__":
    # Example usage: Set GOOGLE_APPLICATION_CREDENTIALS environment variable
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/service-account-key.json"

    consent_texts = [
        "By continuing, you agree to our Terms of Service and Privacy Policy.",
        "This application requests access to your profile information and email address.",
        "Do you consent to share your data with this third-party application?"
    ]
    target_lang = "es"
    source_lang = "en"

    print(f"\n--- Translating consent copy to {target_lang.upper()} ---")
    translated_results = translate_consent_copy(consent_texts, target_lang, source_lang)

    for result in translated_results:
        print(f"Original: {result['input']}")
        print(f"Translated: {result['translated_text']}")
        print(f"Detected Language: {result['detected_source_language']}")
        print("---")
