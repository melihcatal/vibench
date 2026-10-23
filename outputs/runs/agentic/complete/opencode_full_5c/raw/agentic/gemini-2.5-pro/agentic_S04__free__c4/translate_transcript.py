from google.cloud import translate_v2 as translate


def translate_text_segments(segments: list[str], target_language: str) -> list[str]:
    """
    Translates completed transcript segments using Google Cloud Translate.
    """
    translate_client = translate.Client()
    results = [
        result["translatedText"]
        for result in translate_client.translate(
            segments, target_language=target_language
        )
    ]
    return results
