import boto3

translate = boto3.client("translate", region_name="us-west-2")


def translate_markup(markup, source_language, target_language):
    result = translate.translate_text(
        Text=markup,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return result["TranslatedText"]
