import boto3

def summarize_asset(bucket_name, object_key):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_dominant_language(Text=object_key)
    language_code = response['Languages'][0]['LanguageCode']
    
    response = comprehend.detect_sentiment(Text=object_key, LanguageCode=language_code)
    sentiment = response['Sentiment']
    
    response = comprehend.detect_entities(Text=object_key, LanguageCode=language_code)
    entities = response['Entities']
    
    summary = {
        'sentiment': sentiment,
        'entities': entities
    }
    return summary