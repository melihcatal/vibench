import boto3

def check_unsafe_text(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return True
    return False

if __name__ == '__main__':
    sample_text = 'This is a sample text to check for unsafe content.'
    if check_unsafe_text(sample_text):
        print('The text contains unsafe content.')
    else:
        print('The text is safe.')