import boto3

def batch_translate(texts, source_lang, target_lang):
    client = boto3.client('translate')
    results = client.translate_text(Text=texts, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return [result['TranslatedText'] for result in results['TranslatedTexts']]