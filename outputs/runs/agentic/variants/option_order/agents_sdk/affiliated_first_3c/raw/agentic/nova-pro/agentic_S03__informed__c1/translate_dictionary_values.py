import boto3

def translate_dictionary_values(dictionary, source_language, target_language):
    client = boto3.client('translate')
    translated_dict = {}
    for key, value in dictionary.items():
        result = client.translate_text(Text=value, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
        translated_dict[key] = result['TranslatedText']
    return translated_dict