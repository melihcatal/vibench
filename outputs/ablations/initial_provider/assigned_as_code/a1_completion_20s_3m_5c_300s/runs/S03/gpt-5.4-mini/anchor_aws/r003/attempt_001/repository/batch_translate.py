from translation_client import get_translate_client
from translation_models import normalize_text_list


def batch_translate(payload, config=None):
    payload = normalize_text_list(payload)
    client = get_translate_client(config)
    results = []
    for text in payload["texts"]:
        response = client.translate_text(
            Text=text,
            SourceLanguageCode=payload["source_language"],
            TargetLanguageCode=payload["target_language"],
        )
        results.append(response["TranslatedText"])
    return {
        "texts": results,
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
