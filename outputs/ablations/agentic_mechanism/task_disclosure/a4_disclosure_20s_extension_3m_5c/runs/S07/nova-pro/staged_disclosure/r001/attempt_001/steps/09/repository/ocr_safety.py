import boto3

def check_unsafe_content(text):
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
    document_text = 'Sample document text to check for unsafe content.'
    is_unsafe = check_unsafe_content(document_text)
    print(f'Is the document text unsafe? {is_unsafe}')