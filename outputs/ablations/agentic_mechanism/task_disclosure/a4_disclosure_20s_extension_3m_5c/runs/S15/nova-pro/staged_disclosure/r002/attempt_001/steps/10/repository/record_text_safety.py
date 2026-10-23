import boto3

def check_unsafe_content(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(
        Text=text,
        LanguageCode='en'
    )
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return True
    return False

if __name__ == '__main__':
    document_fields = ["This is a safe text.", "This text contains profanity and should be flagged."]
    for field in document_fields:
        if check_unsafe_content(field):
            print(f'Unsafe content detected in: {field}')
        else:
            print(f'Safe content: {field}')
