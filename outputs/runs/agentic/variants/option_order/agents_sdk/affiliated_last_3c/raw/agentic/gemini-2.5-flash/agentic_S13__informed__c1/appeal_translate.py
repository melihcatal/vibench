import os
from google.cloud import translate_v2 as translate

def appeal_translate(text: str, target_language: str = "en") -> dict:
    """
    Translates appeal text for review using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set for authentication.
    """
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable must be set for Google Cloud Translation.")

    translate_client = translate.Client()

    try:
        result = translate_client.translate(text, target_language=target_language)
        return {
            "original_text": text,
            "translated_text": result["translatedText"],
            "source_language": result["detectedSourceLanguage"],
            "target_language": target_language
        }
    except Exception as e:
        return {"error": f"Error translating text: {e}", "original_text": text}

if __name__ == '__main__':
    # Example usage - ensure GOOGLE_APPLICATION_CREDENTIALS is set
    # print(appeal_translate("Hola, me gustaría apelar esta decisión.", target_language="en"))
    # print(appeal_translate("Ich stimme dem nicht zu.", target_language="en"))
    pass
