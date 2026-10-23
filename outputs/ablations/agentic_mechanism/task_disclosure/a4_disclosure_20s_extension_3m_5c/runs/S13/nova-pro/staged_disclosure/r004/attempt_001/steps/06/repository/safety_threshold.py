import boto3

def apply_thresholds(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']
    score = response['SentimentScore'][sentiment]
    thresholds = {
        'POSITIVE': 0.5,
        'NEGATIVE': 0.3,
        'NEUTRAL': 0.5,
        'MIXED': 0.5
    }
    if score >= thresholds[sentiment.upper()]:
        return True
    else:
        return False

if __name__ == '__main__':
    text = 'Your text here'
    if apply_thresholds(text):
        print('Text allowed')
    else:
        print('Text not allowed')