import boto3

def summarize_moderation_decisions(decisions):
    comprehend = boto3.client('comprehend')
    summaries = []
    for decision in decisions:
        result = comprehend.detect_sentiment(Text=decision, LanguageCode='en')
        summaries.append(result['Sentiment'])
    return summaries