import boto3

def summarize_asset(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']
    return sentiment

if __name__ == '__main__':
    text = 'This is the content extracted from the stored asset.'
    summary = summarize_asset(text)
    print(f'The sentiment of the asset is: {summary}')