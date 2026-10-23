import boto3

def translate_dictionary_values(dictionary, source_lang, target_lang):
    client = boto3.client('translate')
    translated_dict = {}
    for key, value in dictionary.items():
        translated_dict[key] = client.translate_text(Text=value, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)['TranslatedText']
    return translated_dict