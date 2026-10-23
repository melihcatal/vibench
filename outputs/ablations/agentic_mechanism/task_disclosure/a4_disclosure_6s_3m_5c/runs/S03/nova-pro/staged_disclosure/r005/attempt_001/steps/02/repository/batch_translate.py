import boto3

def batch_translate(texts, source_lang, target_lang):
    translate = boto3.client('translate')
    results = []
    for text in texts:
        response = translate.translate_text(Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
        results.append(response['TranslatedText'])
    return results

if __name__ == '__main__':
    texts = ['Hello, world!', 'How are you?', 'Thank you.']
    source_lang = 'en'
    target_lang = 'es'
    translated_texts = batch_translate(texts, source_lang, target_lang)
    for original, translated in zip(texts, translated_texts):
        print(f'{original} -> {translated}')
