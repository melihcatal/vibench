import boto3

comprehend = boto3.client('comprehend')

def apply_thresholds(text, thresholds):
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']
    score = response['SentimentScore'][sentiment]
    return score >= thresholds[sentiment]

if __name__ == '__main__':
    text = 'Sample text to evaluate.'
    thresholds = {'POSITIVE': 0.5, 'NEGATIVE': 0.3, 'NEUTRAL': 0.4, 'MIXED': 0.4}
    result = apply_thresholds(text, thresholds)
    print(f'Text allowed: {result}')