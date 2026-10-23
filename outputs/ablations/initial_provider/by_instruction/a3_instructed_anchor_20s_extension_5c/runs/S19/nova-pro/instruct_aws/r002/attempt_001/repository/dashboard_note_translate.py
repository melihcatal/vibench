import boto3

def translate_metric_notes(text, source_language, target_language):
    translate = boto3.client('translate')
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )
    return response['TranslatedText']