import boto3

def summarize_message(message):
    comprehend = boto3.client('comprehend')
    sentiment = comprehend.detect_sentiment(Text=message, LanguageCode='en')
    return sentiment['Sentiment']

if __name__ == '__main__':
    message = 'Your message here'
    summary = summarize_message(message)
    print(f'Message summary: {summary}')