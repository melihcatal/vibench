import boto3

def translate_text(text, source_language_code, target_language_code):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode=source_language_code, TargetLanguageCode=target_language_code)
    return result.translatedText

if __name__ == '__main__':
    sample_text = 'Hello, world!'
    translated_text = translate_text(sample_text, 'en', 'es')
    print(translated_text)