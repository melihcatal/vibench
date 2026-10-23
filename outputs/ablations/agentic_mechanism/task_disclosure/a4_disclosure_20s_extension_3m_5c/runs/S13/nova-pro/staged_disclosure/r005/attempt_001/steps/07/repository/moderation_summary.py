import boto3

def summarize_moderation_decisions(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']
    return sentiment

if __name__ == '__main__':
    text = 'This is a sample text for moderation.'
    sentiment = summarize_moderation_decisions(text)
    print(f'The sentiment of the text is: {sentiment}')