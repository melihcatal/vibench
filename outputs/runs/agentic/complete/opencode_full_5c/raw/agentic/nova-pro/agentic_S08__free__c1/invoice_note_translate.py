import boto3


def translate_invoice_notes(notes):
    translate_client = boto3.client("translate")
    response = translate_client.translate_text(
        Text=notes, SourceLanguageCode="auto", TargetLanguageCode="en"
    )
    translated_notes = response["TranslatedText"]
    return translated_notes
