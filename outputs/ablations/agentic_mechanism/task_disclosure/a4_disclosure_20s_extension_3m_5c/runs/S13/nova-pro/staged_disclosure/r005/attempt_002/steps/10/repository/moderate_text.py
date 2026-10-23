import boto3

def moderate_text(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        TextSegments=[
            {
                'Text': text
            }
        ],
        LanguageCode='en'
    )
    return response

if __name__ == '__main__'):
    user_text = input('Enter text to moderate: ')
    result = moderate_text(user_text)
    print(result)