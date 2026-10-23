import boto3

def translate_dictionary_values(dictionary, source_language, target_language):
    translate_client = boto3.client('translate', region_name='us-east-1')
    translated_dict = {}
    for key, value in dictionary.items():
        result = translate_client.translate_text(Text=value, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
        translated_dict[key] = result['TranslatedText']
    return translated_dict

# Example usage
example_dict = {'hello': 'hello', 'world': 'world'}
translated_dict = translate_dictionary_values(example_dict, 'en', 'es')
print(translated_dict)