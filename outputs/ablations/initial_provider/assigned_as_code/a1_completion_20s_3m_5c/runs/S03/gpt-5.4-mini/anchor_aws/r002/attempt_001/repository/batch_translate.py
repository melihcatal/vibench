import boto3

from translation_models import normalize_batch_payload, normalize_result


def batch_translate(payload, config=None):
    request = normalize_batch_payload(payload)
    client = boto3.client("translate", region_name=(config or {}).get("region"))
    texts = request["texts"]
    source_language = request["source_language"]
    target_language = request["target_language"]
    output = []
    for text in texts:
        response = client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )
        output.append(normalize_result(response["TranslatedText"], source_language, target_language))
    return output
