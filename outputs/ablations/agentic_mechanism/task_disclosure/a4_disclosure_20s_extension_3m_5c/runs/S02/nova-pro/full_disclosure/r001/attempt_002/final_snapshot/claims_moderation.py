import boto3

def moderate_claims(text):
    comprehend = boto3.client('comprehend')
    sentiment = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    entities = comprehend.detect_entities(Text=text, LanguageCode='en')
    key_phrases = comprehend.detect_key_phrases(Text=text, LanguageCode='en')
    
    moderation_result = {
        'sentiment': sentiment,
        'entities': entities,
        'key_phrases': key_phrases
    }
    return moderation_result
