import boto3


def translate_invoice_note(note):
    translate = boto3.client("translate")
    response = translate.translate_text(
        Text=note, SourceLanguageCode="en", TargetLanguageCode="es"
    )
    return response["TranslatedText"]
