import boto3

comprehend = boto3.client('comprehend')

def moderate_profile_text(text):
    response = comprehend.detect_toxic_content(
        Text=text,
        LanguageCode='en'
    )
    if response['ToxicContentDetected']:
        return 'Profile text contains toxic content.'
    else:
        return 'Profile text is acceptable.'

if __name__ == '__main__':
    profile_text = 'Sample profile text to moderate.'
    result = moderate_profile_text(profile_text)
    print(result)