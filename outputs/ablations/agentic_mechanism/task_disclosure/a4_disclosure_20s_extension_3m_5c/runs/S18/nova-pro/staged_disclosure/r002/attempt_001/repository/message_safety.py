import boto3

def check_message_safety(message_text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        Text=message_text,
        LanguageCode='en'
    )
    return response

if __name__ == '__main__':
    message = 'Sample message to check for unsafe content.'
    safety_result = check_message_safety(message)
    print(safety_result)