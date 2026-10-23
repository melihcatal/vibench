import boto3

def check_unsafe_content(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(
        Text=text,
        LanguageCode='en'
    )
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return 'Unsafe content detected'
    else:
        return 'Safe content'

if __name__ == '__main__':\n    text = 'Sample document text to check for unsafe content.'
    result = check_unsafe_content(text)
    print(result)