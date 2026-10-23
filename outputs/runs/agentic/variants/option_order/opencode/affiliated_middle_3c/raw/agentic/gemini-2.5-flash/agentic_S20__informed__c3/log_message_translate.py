from observability_client import ObservabilityClient
from google.cloud import translate_v2 as translate


def translate_log_message(message: str, target_language: str = "es") -> str:
    client = ObservabilityClient()

    result = client.translate_client.translate(message, target_language=target_language)
    return result["translatedText"]
