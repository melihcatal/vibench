import boto3

def check_unsafe_content(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        TextSegments=[{
            'Text': text
        }],
        LanguageCode='en'
    )
    return response

if __name__ == '__main__':
    text = 'Sample text to check for unsafe content.'
    result = check_unsafe_content(text)
    print(result)