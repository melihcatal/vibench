import boto3

translate = boto3.client("translate", region_name="us-west-2")


def translate_transcript(transcript):
    response = translate.translate_text(
        Text=transcript, SourceLanguageCode="en", TargetLanguageCode="es"
    )
    return response["TranslatedText"]
