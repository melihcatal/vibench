import boto3


def translate_script(script):
    translate_client = boto3.client("translate")
    result = translate_client.translate_text(
        Text=script, SourceLanguageCode="auto", TargetLanguageCode="es"
    )
    return result["TranslatedText"]
