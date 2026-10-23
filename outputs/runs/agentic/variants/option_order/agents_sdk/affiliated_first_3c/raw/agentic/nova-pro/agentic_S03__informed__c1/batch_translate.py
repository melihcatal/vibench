import boto3

def batch_translate(texts, source_language, target_language):
    client = boto3.client('translate')
    results = []
    for text in texts:
        result = client.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
        results.append(result['TranslatedText'])
    return results