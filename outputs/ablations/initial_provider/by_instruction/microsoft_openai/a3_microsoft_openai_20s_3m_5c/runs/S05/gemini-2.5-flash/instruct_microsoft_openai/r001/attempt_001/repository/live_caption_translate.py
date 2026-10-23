import os
from google.cloud import translate_v2 as translate

# Google Cloud credentials are typically handled by GOOGLE_APPLICATION_CREDENTIALS
# environment variable or automatically by the client library in a GCP environment.
# For local development, ensure GOOGLE_APPLICATION_CREDENTIALS is set.

def translate_live_caption(text: str, target_language: str = "es") -> dict:
    """
    Translates a live caption text into another language using Google Cloud Translation API.
    """
    if not text:
        return {"translated_text": "", "detected_source_language": None}

    client = translate.Client()

    print(f"Translating '{text}' to {target_language} using Google Cloud Translation...")
    result = client.translate(text, target_language=target_language)

    translated_text = result["translatedText"]
    detected_source_language = result["detectedSourceLanguage"]

    return {
        "translated_text": translated_text,
        "detected_source_language": detected_source_language
    }

if __name__ == "__main__":
    # This is a placeholder for a live caption stream.
    # In a real application, this would receive captions from a speech-to-text service.
    dummy_live_captions = [
        "Hello, how are you today?",
        "The weather is really nice.",
        "This is a test of the translation service."
    ]

    print("Starting live caption translation simulation...")
    for caption in dummy_live_captions:
        translation_result = translate_live_caption(caption, target_language="fr")
        print(f"Original: '{caption}'")
        print(f"Translated (FR): '{translation_result['translated_text']}' (Detected source: {translation_result['detected_source_language']})")
        print("---")
