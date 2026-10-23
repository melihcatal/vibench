import boto3


def translate_transcript(payload, config=None):
    client = boto3.client("translate", region_name=(config or {}).get("region"))
    text = payload["text"]
    response = client.translate_text(Text=text, SourceLanguageCode=payload["source_language"], TargetLanguageCode=payload["target_language"])
    return {"translated_text": response["TranslatedText"], "source_language": response["SourceLanguageCode"], "target_language": response["TargetLanguageCode"]}
