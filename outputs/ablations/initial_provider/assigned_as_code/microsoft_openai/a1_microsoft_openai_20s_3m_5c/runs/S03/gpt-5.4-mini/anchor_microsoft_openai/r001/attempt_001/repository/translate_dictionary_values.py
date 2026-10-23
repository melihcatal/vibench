from translation_client import MicrosoftTranslatorClient


def translate_dictionary_values(payload, config=None):
    config = config or {}
    client = MicrosoftTranslatorClient(
        api_key=config.get("api_key"),
        region=config.get("region"),
        endpoint=config.get("endpoint"),
    )
    result = {}
    for key, value in payload["values"].items():
        result[key] = client.translate(str(value), payload["source_language"], payload["target_language"])["text"]
    return {"values": result, "source_language": payload["source_language"], "target_language": payload["target_language"]}
