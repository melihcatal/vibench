import boto3

comprehend = boto3.client('comprehend')

def check_script(script_text):
    response = comprehend.detect_sentiment(
        Text=script_text,
        LanguageCode='en'
    )
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return 'Unsafe content detected'
    else:
        return 'Safe content'

if __name__ == '__main__':
    script_text = 'This is a sample narration script.'
    result = check_script(script_text)
    print(result)