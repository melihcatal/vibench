import boto3

translate = boto3.client('translate')

def translate_dashboard_note(text, source_language, target_language):
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )
    return response['TranslatedText']