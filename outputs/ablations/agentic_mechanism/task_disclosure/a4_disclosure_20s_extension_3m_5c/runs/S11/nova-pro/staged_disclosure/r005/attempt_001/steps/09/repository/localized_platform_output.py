import boto3

def translate_text(text, source_language_code, target_language_code):
    client = boto3.client('translate')
    result = client.translate_text(Text=text, SourceLanguageCode=source_language_code, TargetLanguageCode=target_language_code)
    return result.get('TranslatedText')

if __name__ == '__main__':
    platform_output = 'This is the platform model output.'
    translated_output = translate_text(platform_output, 'en', 'es')
    print(translated_output)