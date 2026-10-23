import boto3

def check_unsafe_text(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return True
    return False

def main():
    secret_label = 'Example secret label'
    secret_note = 'Example secret note'
    if check_unsafe_text(secret_label):
        print('Unsafe text detected in secret label')
    if check_unsafe_text(secret_note):
        print('Unsafe text detected in secret note')

if __name__ == '__main__':
    main()