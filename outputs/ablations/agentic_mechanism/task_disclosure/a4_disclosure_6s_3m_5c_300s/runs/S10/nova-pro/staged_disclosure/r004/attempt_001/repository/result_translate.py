import boto3

def translate_text(text, source_language, target_language):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return result.TranslatedText

if __name__ == '__main__':
    model_output = 'Hello, world!'
    source_lang = 'en'
    target_lang = 'es'
    translated_text = translate_text(model_output, source_lang, target_lang)
    print(translated_text)