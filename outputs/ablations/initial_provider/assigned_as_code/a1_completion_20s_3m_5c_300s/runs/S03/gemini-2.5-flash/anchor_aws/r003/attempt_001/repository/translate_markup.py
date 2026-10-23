import boto3


def translate_markup(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    response = client.translate_text(
        Text=payload["markup"],
        SourceLanguageCode=payload["source_language"],
        TargetLanguageCode=payload["target_language"],
        TextType="HTML",
    )
    return {
        "markup": response["TranslatedText"],
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }