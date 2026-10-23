from translation_client import MicrosoftTranslatorClient
from translation_models import normalize_string_list


def batch_translate(payload, config=None):
    config = config or {}
    client = MicrosoftTranslatorClient(
        api_key=config.get("api_key"),
        region=config.get("region"),
        endpoint=config.get("endpoint"),
    )
    texts = normalize_string_list(payload.get("texts"))
    results = []
    for text in texts:
        translated = client.translate(text, payload["source_language"], payload["target_language"])
        results.append(translated["text"])
    return {"texts": results, "source_language": payload["source_language"], "target_language": payload["target_language"]}
