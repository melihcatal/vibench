import boto3

from storage_models import normalize_object_name


def stored_text_translate(payload, config=None):
    config = dict(config or {})
    s3 = boto3.client("s3", region_name=config.get("region"))
    body = s3.get_object(Bucket=config["bucket"], Key=normalize_object_name(payload["object_name"]))["Body"].read().decode("utf-8")
    translate = boto3.client("translate", region_name=config.get("region"))
    response = translate.translate_text(
        Text=body,
        SourceLanguageCode=payload.get("source_language", "auto"),
        TargetLanguageCode=payload["target_language"],
    )
    return {"translated_text": response["TranslatedText"], "source_language": response["SourceLanguageCode"]}
