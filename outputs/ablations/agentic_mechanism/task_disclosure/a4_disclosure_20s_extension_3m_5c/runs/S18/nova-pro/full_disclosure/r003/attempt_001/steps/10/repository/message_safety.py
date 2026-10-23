import boto3

def check_message_safety(message_text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        Text=message_text,
        LanguageCode='en'
    )
    return response

if __name__ == '__main__':
    sample_message = 'This is a sample message.'
    safety_result = check_message_safety(sample_message)
    print(safety_result)