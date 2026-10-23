from observability_client import ObservabilityClient

def translate_dashboard_note(text: str, target_language: str = "es") -> str:
    client = ObservabilityClient()

    # The target_language should be an ISO 639-1 code (e.g., 'es' for Spanish)
    translation = client.translate_client.translate(
        text,
        target_language=target_language
    )

    return translation['translatedText']
