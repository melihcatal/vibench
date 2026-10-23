import boto3

def translate_dashboard_note(note, source_language, target_language):
    client = boto3.client('translate')
    response = client.translate_text(
        Text=note,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )
    return response