import boto3

def translate_dictionary_values(dictionary, source_language, target_language):
    translate = boto3.client('translate', region_name='us-west-2')
    translated_dict = {}
    for key, value in dictionary.items():
        result = translate.translate_text(Text=value, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
        translated_dict[key] = result.translatedText
    return translated_dict