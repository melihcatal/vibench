import boto3

def batch_translate(texts, source_language, target_language):
    client = boto3.client('translate')
    responses = []
    for text in texts:
        response = client.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
        responses.append(response['TranslatedText'])
    return responses