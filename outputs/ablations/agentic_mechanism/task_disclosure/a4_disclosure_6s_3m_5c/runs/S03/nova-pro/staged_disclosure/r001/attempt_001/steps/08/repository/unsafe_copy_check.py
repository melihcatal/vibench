import boto3

def check_unsafe_content(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return True
    else:
        return False

if __name__ == '__main__':
    localized_copy = 'Your localized copy here'
    if check_unsafe_content(localized_copy):
        print('Unsafe content detected!')
    else:
        print('No unsafe content detected.')