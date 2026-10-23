import boto3

def check_unsafe_text(text):
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
    example_text = 'This is a dangerous and harmful annotation.'
    is_unsafe = check_unsafe_text(example_text)
    print(f'Is the text unsafe? {is_unsafe}')