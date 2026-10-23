from google.cloud import translate_v2 as translate
import os


def translate_transcript(transcript_text, target_language="es"):
    """Translate completed transcript segments using Google Cloud Translation API."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set"
        )

    client = translate.Client()

    if isinstance(transcript_text, list):
        # Translate list of segments
        translations = []
        for segment in transcript_text:
            result = client.translate(
                segment, target_language=target_language, format_="text"
            )
            translations.append(result["translatedText"])
        return translations
    else:
        # Translate single text
        result = client.translate(
            transcript_text, target_language=target_language, format_="text"
        )
        return result["translatedText"]
