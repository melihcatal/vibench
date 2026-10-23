import os
from google.cloud import translate_v2 as translate
from speech_models import TranslatedSegment

def translate_transcript_segment(text: str, target_language: str, source_language: Optional[str] = None) -> TranslatedSegment:
    """Translates a single transcript segment using Google Cloud Translation."""
    # Google Cloud client libraries automatically use GOOGLE_APPLICATION_CREDENTIALS
    # if set, or other default credentials.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # authentication is configured otherwise.

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language, source_language=source_language)

    return TranslatedSegment(
        original_text=text,
        translated_text=result["translatedText"],
        source_language=result["detectedSourceLanguage"] if "detectedSourceLanguage" in result else source_language or "unknown",
        target_language=target_language
    )

if __name__ == "__main__":
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS setup)
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"
    # 
    # try:
    #     segment_to_translate = "Hello world, this is a test segment."
    #     translated = translate_transcript_segment(segment_to_translate, "es")
    #     print(f"Original: {translated.original_text}")
    #     print(f"Translated ({translated.source_language} -> {translated.target_language}): {translated.translated_text}")
    # except Exception as e:
    #     print(f"Error translating: {e}")
    pass
