def appeal_translate(appeal_text, target_language='es'):
    translate = boto3.client('translate')
    response = translate.translate_text(
        Text=appeal_text,
        SourceLanguageCode='en',
        TargetLanguageCode=target_language
    )
    return response['TranslatedText']