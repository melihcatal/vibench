import boto3

def batch_translate(texts, source_language, target_language):
    translate = boto3.client('translate', region_name='us-west-2')
    results = []
    for text in texts:
        result = translate.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
        results.append(result.translatedText)
    return results