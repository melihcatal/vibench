import boto3

def summarize_moderation_decisions(decisions):
    comprehend = boto3.client('comprehend')
    summaries = []
    for decision in decisions:
        response = comprehend.detect_sentiment(
            Text=decision['text'],
            LanguageCode='en'
        )
        summaries.append({
            'text': decision['text'],
            'sentiment': response['Sentiment'],
            'sentiment_score': response['SentimentScore']
        })
    return summaries