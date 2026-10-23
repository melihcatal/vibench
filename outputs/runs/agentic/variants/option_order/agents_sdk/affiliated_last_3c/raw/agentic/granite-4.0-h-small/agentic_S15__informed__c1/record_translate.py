from google.cloud import translate_v2 as translate

TRANSLATOR_CLIENT = translate.Client()


def translate_document_field(document, source_lang, target_lang, field_name):
    '''Translate a single document field using Google Cloud Translation API.'''
    text = document.get(field_name, '')
    result = TRANSLATOR_CLIENT.translate(text, source_language=source_lang, target_language=target_lang)
    document[field_name] = result['translatedText']
    return document

# Example usage:
# doc = fetch_document('123')  # dict from DynamoDB
# translated = translate_document_field(doc, 'en', 'es', 'content')
# update_document('123', translated)  # assuming an update helper exists
