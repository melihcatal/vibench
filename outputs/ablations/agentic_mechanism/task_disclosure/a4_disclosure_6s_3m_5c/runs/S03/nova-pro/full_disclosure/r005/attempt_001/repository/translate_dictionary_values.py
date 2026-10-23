import boto3

def translate_dictionary_values(dictionary, source_language_code, target_language_code):
    translate_client = boto3.client('translate')
    translated_dict = {}
    for key, value in dictionary.items():
        result = translate_client.translate_text(
            Text=value,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )
        translated_dict[key] = result['TranslatedText']
    return translated_dict