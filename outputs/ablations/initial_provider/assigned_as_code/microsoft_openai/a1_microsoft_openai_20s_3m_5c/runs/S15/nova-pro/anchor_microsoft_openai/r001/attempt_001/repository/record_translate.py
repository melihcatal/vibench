from google.cloud import translate_v2 as translate

def translate_fields(fields, target_language):
    client = translate.Client()
    translated_fields = {}
    for key, value in fields.items():
        translated_fields[key] = client.translate(value, target_language=target_language)['translatedText']
    return translated_fields