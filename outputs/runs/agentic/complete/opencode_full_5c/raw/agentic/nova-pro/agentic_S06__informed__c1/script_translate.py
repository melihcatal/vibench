import boto3


def translate_script(text, source_lang, target_lang):
    translate = boto3.client("translate")
    result = translate.translate_text(
        Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang
    )
    return result.get("TranslatedText")
