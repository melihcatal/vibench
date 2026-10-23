import boto3

def summarize_moderation_decisions(text):
    comprehend = boto3.client('comprehend')
    sentiment = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return sentiment['Sentiment']

if __name__ == '__main__':
    text = 'Example text for moderation decision.'
    summary = summarize_moderation_decisions(text)
    print(f'Moderation decision summary: {summary}')
