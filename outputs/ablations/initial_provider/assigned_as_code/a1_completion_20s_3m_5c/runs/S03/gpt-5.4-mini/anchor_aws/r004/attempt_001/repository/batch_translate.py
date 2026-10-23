from translation_client import create_translation_client, translate_with_client
from translation_models import normalize_text_list


def batch_translate(payload, config=None):
    config = config or {}
    client = create_translation_client(config)
    texts = normalize_text_list(payload["texts"])
    results = [
        translate_with_client(
            client,
            text,
            payload["source_language"],
            payload["target_language"],
        )["text"]
        for text in texts
    ]
    return {
        "texts": results,
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
