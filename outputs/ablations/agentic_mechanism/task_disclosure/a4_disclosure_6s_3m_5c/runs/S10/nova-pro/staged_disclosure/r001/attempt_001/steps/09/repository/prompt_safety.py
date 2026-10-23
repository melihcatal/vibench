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
    prompt = 'This is a sample prompt.'
    generated_text = 'This is a sample generated text.'
    if check_unsafe_content(prompt) or check_unsafe_content(generated_text):
        print('Unsafe content detected!')
    else:
        print('No unsafe content detected.')