from translation_client import MicrosoftTranslatorClient
from translation_models import extract_markup_segments, inject_translated_segments


def translate_markup(payload, config=None):
    config = config or {}
    client = MicrosoftTranslatorClient(
        api_key=config.get("api_key"),
        region=config.get("region"),
        endpoint=config.get("endpoint"),
    )
    segments = extract_markup_segments(payload["markup"])
    translated_segments = [client.translate(segment, payload["source_language"], payload["target_language"])["text"] for segment in segments]
    return {"markup": inject_translated_segments(payload["markup"], translated_segments), "source_language": payload["source_language"], "target_language": payload["target_language"]}
