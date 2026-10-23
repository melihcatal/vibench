import os
from google.cloud import translate_v2 as translate


def translate_text_segments(
    segments: list[str], target_language: str = "es"
) -> list[str]:
    """
    Translate completed transcript segments using Google Cloud Translate.
    """
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise EnvironmentError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable not set."
        )

    translate_client = translate.Client()

    results = []
    for segment in segments:
        result = translate_client.translate(segment, target_language=target_language)
        results.append(result["translatedText"])

    return results
