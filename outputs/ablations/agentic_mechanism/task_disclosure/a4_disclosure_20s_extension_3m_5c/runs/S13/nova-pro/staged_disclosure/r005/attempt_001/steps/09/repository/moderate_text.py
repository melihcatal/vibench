import boto3

def moderate_text(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(
        Text=text,
        LanguageCode='en'
    )
    return response

if __name__ == '__main__':
    user_text = 'Enter text to be moderated.'
    result = moderate_text(user_text)
    print(result)