import boto3


def payload_translate(payload, config=None):
    config = config or {}
    translate = boto3.client("translate", region_name=config.get("region"))
    text = payload.get("text") or payload.get("message") or ""
    target = payload.get("target_language", "es")
    response = translate.translate_text(Text=text, SourceLanguageCode="auto", TargetLanguageCode=target)
    return {"translated_text": response.get("TranslatedText"), "target_language": target}
