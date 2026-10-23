import boto3

def batch_translate(texts, source_lang, target_lang):
    translate = boto3.client('translate')
    results = []
    for text in texts:
        response = translate.translate_text(Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
        results.append(response['TranslatedText'])
    return results