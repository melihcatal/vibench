import boto3

def check_unsafe_content(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        Text=text,
        LanguageCode='en'
    )
    return response

if __name__ == '__main__':
    sample_text = 'This is a sample text to check for unsafe content.'
    result = check_unsafe_content(sample_text)
    print(result)