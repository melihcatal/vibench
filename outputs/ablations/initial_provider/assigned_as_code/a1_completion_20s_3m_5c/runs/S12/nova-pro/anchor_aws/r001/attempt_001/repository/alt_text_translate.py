import boto3

from vision_client import get_vision_client
from vision_models import normalize_translated_text


def alt_text_translate(payload, config=None):
    config = config or {}
    client = get_vision_client(config)
    description = client.detect_labels(
        Image={"Bytes": payload["image_bytes"]},
        MaxLabels=int(config.get("max_labels", 10)),
    )["Labels"][0]["Name"]
    translate_client = boto3.client("translate", region_name=config.get("region", "us-west-2"))
    response = translate_client.translate_text(
        Text=description,
        SourceLanguageCode="en",
        TargetLanguageCode=config.get("target_language", "es"),
    )
    return normalize_translated_text(response["TranslatedText"])