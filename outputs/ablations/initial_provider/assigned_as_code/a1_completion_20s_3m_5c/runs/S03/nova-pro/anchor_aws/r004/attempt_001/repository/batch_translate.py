import boto3


def batch_translate(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    texts = payload["texts"]
    source_language = payload["source_language"]
    target_language = payload["target_language"]
    responses = []
    for text in texts:
        response = client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )
        responses.append({
            "text": response["TranslatedText"],
            "source_language": source_language,
            "target_language": target_language,
        })
    return responses