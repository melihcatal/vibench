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
    transcript_text = 'Your live transcript text here'
    is_unsafe = check_unsafe_content(transcript_text)
    if is_unsafe:
        print('Unsafe content detected!')
    else:
        print('No unsafe content detected.')