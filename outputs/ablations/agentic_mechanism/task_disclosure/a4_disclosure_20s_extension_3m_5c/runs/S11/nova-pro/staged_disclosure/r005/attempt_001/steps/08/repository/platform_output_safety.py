import boto3

def check_unsafe_content(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        TextSegments=[
            {
                'Text': text
            }
        ]
    )
    return response

if __name__ == '__main__':\n    text_to_check = 'Example text to check for unsafe content.'
    result = check_unsafe_content(text_to_check)
    print(result)