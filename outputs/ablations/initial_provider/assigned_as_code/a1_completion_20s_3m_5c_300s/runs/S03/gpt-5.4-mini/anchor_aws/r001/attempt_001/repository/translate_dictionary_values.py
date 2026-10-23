from translation_client import get_translation_client, translate_with_client
from translation_models import normalize_payload


def translate_dictionary_values(payload, config=None):
    payload = normalize_payload(payload)
    client = get_translation_client(config)
    values = {
        key: translate_with_client(client, value, payload["source_language"], payload["target_language"])
        for key, value in payload["values"].items()
    }
    return {
        "values": values,
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
