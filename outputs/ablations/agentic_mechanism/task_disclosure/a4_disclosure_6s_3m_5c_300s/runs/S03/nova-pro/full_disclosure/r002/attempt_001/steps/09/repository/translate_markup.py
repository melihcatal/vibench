import boto3


def translate_markup(text, source_language_code, target_language_code):
    client = boto3.client('translate')
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code,
        TerminologyNames=[]
    )
    return response['TranslatedText']