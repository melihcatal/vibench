import boto3

from embeddings_client import get_config


def multilingual_query_translate(payload, config=None):
    config = get_config(config)
    client = boto3.client("translate", region_name=config["region"])
    response = client.translate_text(Text=payload["query"], SourceLanguageCode=payload.get("source_language", "auto"), TargetLanguageCode=payload.get("target_language", "en"))
    return {"translated_query": response["TranslatedText"]}
