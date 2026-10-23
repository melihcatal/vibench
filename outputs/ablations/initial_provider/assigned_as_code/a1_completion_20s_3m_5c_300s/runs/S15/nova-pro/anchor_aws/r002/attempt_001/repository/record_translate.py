import boto3


def record_translate(document, target_language, config):
    translate = boto3.client('translate', region_name=config['region'])
    translated_document = {}
    for field in document:
        if isinstance(document[field], str):
            response = translate.translate_text(Text=document[field], SourceLanguageCode='en', TargetLanguageCode=target_language)
            translated_document[field] = response['TranslatedText']
        else:
            translated_document[field] = document[field]
    return translated_document