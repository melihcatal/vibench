import boto3
from storage_client import get_storage_config, get_s3_client
from storage_models import normalize_key


def stored_text_translate(payload, config=None):
    config = get_storage_config(config)
    s3 = get_s3_client(config)
    body = s3.get_object(Bucket=config["bucket"], Key=normalize_key(payload))["Body"].read().decode("utf-8")
    translate = boto3.client("translate", region_name=config.get("region"))
    response = translate.translate_text(Text=body, SourceLanguageCode=payload.get("source_language", "auto"), TargetLanguageCode=payload.get("target_language", "en"))
    return {"translated_text": response["TranslatedText"], "object_name": normalize_key(payload)}
