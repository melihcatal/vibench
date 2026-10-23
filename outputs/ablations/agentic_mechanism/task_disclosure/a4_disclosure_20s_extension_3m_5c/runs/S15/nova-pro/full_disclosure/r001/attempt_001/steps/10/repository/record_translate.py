import boto3

def translate_text(text, source_language_code, target_language_code):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode=source_language_code, TargetLanguageCode=target_language_code)
    return result.TranslatedText

def translate_document_fields(document):
    translated_document = {}
    for key, value in document.items():
        if isinstance(value, str):
            translated_value = translate_text(value, 'en', 'es')
            translated_document[key] = translated_value
        else:
            translated_document[key] = value
    return translated_document