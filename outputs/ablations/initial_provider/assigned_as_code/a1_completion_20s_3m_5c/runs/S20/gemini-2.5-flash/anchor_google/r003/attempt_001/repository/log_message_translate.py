from observability_client import ObservabilityClient

def translate_log_message(log_message_text, target_language_code, config=None):
    config = config or {}
    client = ObservabilityClient(project_id=config["project_id"])
    translate_client = client.get_translate_client()

    translation = translate_client.translate(
        log_message_text, target_language=target_language_code
    )

    return {
        "original_message": log_message_text,
        "translated_message": translation["translatedText"],
        "target_language": target_language_code,
        "detected_source_language": translation["detectedSourceLanguage"],
    }
