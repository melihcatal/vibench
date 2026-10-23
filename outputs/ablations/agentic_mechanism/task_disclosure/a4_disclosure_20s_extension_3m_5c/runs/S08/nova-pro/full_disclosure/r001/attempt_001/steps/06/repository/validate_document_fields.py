import boto3

def validate_fields(document):
    comprehend = boto3.client('comprehend')
    try:
        response = comprehend.detect_sentiment(Text=document['text'], LanguageCode='en')
        sentiment = response['Sentiment']
        confidence_score = response['SentimentScore'][sentiment]
        if confidence_score < 0.5:
            return False, 'Low confidence score'
        else:
            return True, 'Validation passed'
    except Exception as e:
        return False, str(e)