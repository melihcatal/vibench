from safety_client import load_safety_config


def appeal_translate(payload, config=None):
    import boto3

    cfg = load_safety_config(config)
    client = boto3.client("translate", region_name=cfg["region"])
    data = payload or {}
    response = client.translate_text(Text=data.get("text", ""), SourceLanguageCode=data.get("source_language", "auto"), TargetLanguageCode=data.get("target_language", "en"))
    return {"translated_text": response["TranslatedText"], "provider": "aws-translate"}
