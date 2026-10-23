import boto3

def check_unsafe_text(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return True
    return False

if __name__ == '__main__':\n    label = 'Example unsafe text'
    if check_unsafe_text(label):
        print(f'The label contains unsafe text: {label}')
    else:\n        print(f'The label is safe: {label}')
