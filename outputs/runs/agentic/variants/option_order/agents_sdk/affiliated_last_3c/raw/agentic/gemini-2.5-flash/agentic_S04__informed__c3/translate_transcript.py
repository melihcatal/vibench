from google.cloud import translate_v2 as translate
import os

def translate_text_segments(text_segments: list[str], target_language: str = "es") -> list[str]:
    """
    Translates a list of text segments using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set.
    """
    translate_client = translate.Client()

    translated_segments = []
    for segment in text_segments:
        # Target language can be a ISO 639-1 code (e.g. "es" for Spanish)
        translation = translate_client.translate(segment, target_language=target_language)
        translated_segments.append(translation["translatedText"])
        print(f"Translated '{segment}' to '{translation["translatedText"]}' ({target_language})")
    
    return translated_segments
