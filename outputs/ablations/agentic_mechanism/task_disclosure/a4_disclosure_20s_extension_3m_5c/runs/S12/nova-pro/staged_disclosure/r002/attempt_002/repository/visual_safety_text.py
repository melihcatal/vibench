import boto3

def check_unsafe_text(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        TextSegments=[
            {
                'Text': text
            }
        ]
    )
    for result in response['Results']:
        if result['Toxicity']['Label'] == 'TOXIC':
            return True
    return False

if __name__ == '__main__':
    sample_text = 'This is a sample text to check for unsafe content.'
    is_unsafe = check_unsafe_text(sample_text)
    print(f'Is the text unsafe? {is_unsafe}')
