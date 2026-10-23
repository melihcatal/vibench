import boto3

def batch_translate(texts, source_lang, target_lang):
    translate = boto3.client('translate', region_name='us-west-2')
    results = []
    for text in texts:
        result = translate.translate_text(Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
        results.append(result.get('TranslatedText'))
    return results