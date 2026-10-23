import boto3

def check_message_safety(message_text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(
        Text=message_text,
        LanguageCode='en'
    )
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return False
    else:
        return True

if __name__ == '__main__':
    message = 'Your message text here'
    is_safe = check_message_safety(message)
    print(f'Is the message safe? {is_safe}')
