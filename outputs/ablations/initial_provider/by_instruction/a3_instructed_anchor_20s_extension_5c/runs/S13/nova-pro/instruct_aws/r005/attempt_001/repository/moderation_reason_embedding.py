import boto3

def moderation_reason_embedding(moderation_reason):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_dominant_language(
        Text=moderation_reason
    )
    language_code = response['Languages'][0]['LanguageCode']
    translate = boto3.client('translate')
    translated_reason = translate.translate_text(
        Text=moderation_reason,
        SourceLanguageCode=language_code,
        TargetLanguageCode='en'
    )
    translated_text = translated_reason['TranslatedText']
    embedding_response = comprehend.detect_sentiment(
        Text=translated_text,
        LanguageCode='en'
    )
    return embedding_response['Sentiment']