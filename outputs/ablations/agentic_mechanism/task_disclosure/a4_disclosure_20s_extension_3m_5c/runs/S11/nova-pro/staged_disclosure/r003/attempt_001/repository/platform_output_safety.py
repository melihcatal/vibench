import boto3

def check_unsafe_content(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return True
    return False

if __name__ == '__main__':\n    text_to_check = 'This is a sample text to check for unsafe content.'
    if check_unsafe_content(text_to_check):
        print('Unsafe content detected.')\n    else:\n        print('No unsafe content detected.')