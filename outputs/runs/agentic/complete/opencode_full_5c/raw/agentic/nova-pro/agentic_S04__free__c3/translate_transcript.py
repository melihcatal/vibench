import boto3


def translate_transcript(transcript):
    translate = boto3.client("translate")
    response = translate.translate_text(
        Text=transcript, SourceLanguageCode="en", TargetLanguageCode="es"
    )
    return response["TranslatedText"]
