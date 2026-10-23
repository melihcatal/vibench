import boto3

def translate_text(text, source_language, target_language):
    client = boto3.client('translate')
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )
    return response['TranslatedText']

if __name__ == '__main__':
    source_text = 'Hello, world!'
    source_lang = 'en'
    target_lang = 'es'
    translated_text = translate_text(source_text, source_lang, target_lang)
    print(translated_text)