import boto3

comprehend = boto3.client('comprehend')

def check_unsafe_text(text):
    response = comprehend.detect_sentiment(
        Text=text,
        LanguageCode='en'
    )
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return True
    return False

# Example usage
text = 'This is a sample text to check for unsafe content.'
if check_unsafe_text(text):
    print('Unsafe text detected!')
else:
    print('Text is safe.')