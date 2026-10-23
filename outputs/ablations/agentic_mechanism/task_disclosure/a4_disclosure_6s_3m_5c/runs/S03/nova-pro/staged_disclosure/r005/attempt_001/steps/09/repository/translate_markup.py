import boto3

def translate_markup(markup, source_lang, target_lang):
    translate = boto3.client('translate')
    response = translate.translate_text(Text=markup, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return response.get('TranslatedText', '')

if __name__ == '__main__':
    markup = '<html><body><h1>Hello, World!</h1></body></html>'
    source_lang = 'en'
    target_lang = 'es'
    translated_markup = translate_markup(markup, source_lang, target_lang)
    print(translated_markup)