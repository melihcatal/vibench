import boto3

def check_log_message(log_text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(
        Text=log_text,
        LanguageCode='en'
    )
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return 'Unsafe content detected'
    else:
        return 'Safe content'

if __name__ == '__main__':
    log_message = 'Example log message'
    result = check_log_message(log_message)
    print(result)