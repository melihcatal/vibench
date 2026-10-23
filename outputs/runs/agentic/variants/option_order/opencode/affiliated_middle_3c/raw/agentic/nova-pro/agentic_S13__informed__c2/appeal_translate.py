import boto3


def appeal_translate(text, source_lang, target_lang):
    translate = boto3.client(
        "translate",
        aws_access_key_id="AWS_ACCESS_KEY_ID",
        aws_secret_access_key="AWS_SECRET_ACCESS_KEY",
    )
    response = translate.translate_text(
        Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang
    )
    return response.translated_text
