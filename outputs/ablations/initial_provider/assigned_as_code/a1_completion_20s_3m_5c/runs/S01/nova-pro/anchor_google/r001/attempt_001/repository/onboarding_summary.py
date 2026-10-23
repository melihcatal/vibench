import boto3


def summarize_onboarding_state(user_id, onboarding_steps):
    comprehend = boto3.client('comprehend')
    summary = ""
    for step in onboarding_steps:
        result = comprehend.detect_sentiment(Text=step, LanguageCode='en')
        summary += f"{step} - Sentiment: {result.get('Sentiment')}\n"
    return summary