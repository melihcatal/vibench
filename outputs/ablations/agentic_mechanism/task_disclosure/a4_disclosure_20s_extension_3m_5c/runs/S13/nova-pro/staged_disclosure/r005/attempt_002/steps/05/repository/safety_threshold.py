import boto3

def analyze_text(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']
    score = response['SentimentScore'][sentiment]
    return sentiment, score

def is_safe(text, threshold=0.5):
    sentiment, score = analyze_text(text)
    if sentiment == 'POSITIVE' and score > threshold:
        return True
    else:
        return False