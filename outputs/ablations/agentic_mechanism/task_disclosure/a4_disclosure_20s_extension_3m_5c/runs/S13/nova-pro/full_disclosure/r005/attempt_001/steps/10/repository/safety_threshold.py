import boto3

def apply_thresholds(text, thresholds):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']
    sentiment_score = response['SentimentScore']

    decision = {}
    for category, threshold in thresholds.items():
        if category in sentiment_score:
            decision[category] = sentiment_score[category] >= threshold
        else:
            decision[category] = False
    return decision

if __name__ == '__main__':
    sample_text = 'I love this product! It is the best thing ever.'
    sample_thresholds = {'Positive': 0.5, 'Negative': 0.5}
    decision = apply_thresholds(sample_text, sample_thresholds)
    print(decision)