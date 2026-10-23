import boto3

def translate_dictionary_values(dictionary, source_language, target_language):
    client = boto3.client('translate')
    translated_dict = {}
    for key, value in dictionary.items():
        translated_value = client.translate_text(Text=value, SourceLanguageCode=source_language, TargetLanguageCode=target_language)['TranslatedText']
        translated_dict[key] = translated_value
    return translated_dict