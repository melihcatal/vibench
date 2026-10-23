import boto3

def check_unsafe_content(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return True
    return False

if __name__ == '__main__':\n    text = 'Enter text to check for unsafe content'\n    if check_unsafe_content(text):\n        print('Unsafe content detected')\n    else:\n        print('No unsafe content detected')