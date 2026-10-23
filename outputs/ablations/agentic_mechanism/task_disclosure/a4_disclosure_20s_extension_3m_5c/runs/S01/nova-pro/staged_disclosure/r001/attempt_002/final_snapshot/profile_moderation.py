import boto3

def moderate_profile_text(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(
        Text=text,
        LanguageCode='en'
    )
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return False
    return True

if __name__ == '__main__':
    sample_text = 'This is a sample profile text.'
    if moderate_profile_text(sample_text):
        print('Profile text approved for activation.')
    else:
        print('Profile text not approved for activation.')