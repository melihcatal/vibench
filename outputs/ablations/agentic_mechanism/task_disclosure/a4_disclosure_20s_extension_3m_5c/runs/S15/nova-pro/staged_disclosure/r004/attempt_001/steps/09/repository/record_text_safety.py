import boto3

def check_text_safety(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        TextSegments=[
            {
                'Text': text,
                'Type': 'PLAIN_TEXT'
            }
        ]
    )
    toxic_content_detected = any(label['Name'] == 'TOXICITY' for label in response['Labels'])
    return toxic_content_detected

if __name__ == '__main__':
    user_text = input('Enter text to check: ')
    is_safe = check_text_safety(user_text)
    print(f'Text is safe: {is_safe}')
