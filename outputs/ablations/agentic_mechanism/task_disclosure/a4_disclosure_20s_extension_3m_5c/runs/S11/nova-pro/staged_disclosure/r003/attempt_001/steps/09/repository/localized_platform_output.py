import boto3

def translate_text(text, source_language_code, target_language_code):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode=source_language_code, TargetLanguageCode=target_language_code)
    return result.TranslatedText

if __name__ == '__main__':
    platform_output = 'Hello, world!'
    translated_output = translate_text(platform_output, 'en', 'es')
    print(translated_output)