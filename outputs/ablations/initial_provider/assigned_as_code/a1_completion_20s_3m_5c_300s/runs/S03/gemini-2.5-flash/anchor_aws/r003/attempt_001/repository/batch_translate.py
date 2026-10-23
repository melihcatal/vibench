import boto3


def batch_translate(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    translated_texts = []
    for text in payload["texts"]:
        response = client.translate_text(
            Text=text,
            SourceLanguageCode=payload["source_language"],
            TargetLanguageCode=payload["target_language"],
        )
        translated_texts.append(response["TranslatedText"])
    return {
        "texts": translated_texts,
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }