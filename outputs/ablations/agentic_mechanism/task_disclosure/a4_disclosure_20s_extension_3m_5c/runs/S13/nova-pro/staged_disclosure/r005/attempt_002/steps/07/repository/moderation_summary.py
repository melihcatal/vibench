import boto3

def summarize_moderation_decisions(text):
    comprehend = boto3.client('comprehend')
    sentiment = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return sentiment['Sentiment']

if __name__ == '__main__':
    text = 'Sample text for moderation.'
    sentiment = summarize_moderation_decisions(text)
    print(f'Moderation Sentiment: {sentiment}')