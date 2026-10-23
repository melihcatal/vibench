import boto3

def translate_text(text, source_lang, target_lang):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return result.TranslatedText

if __name__ == '__main__':
    sample_text = 'Hello, world!'
    source_language = 'en'
    target_language = 'es'
    translated_text = translate_text(sample_text, source_language, target_language)
    print(translated_text)