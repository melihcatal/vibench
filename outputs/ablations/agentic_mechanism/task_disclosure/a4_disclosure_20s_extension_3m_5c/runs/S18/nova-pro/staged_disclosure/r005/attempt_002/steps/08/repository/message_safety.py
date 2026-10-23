import boto3

def check_message_safety(message_text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        Text=message_text,
        LanguageCode='en'
    )
    return response

if __name__ == '__main__':
    message = 'Your message text goes here.'
    safety_check = check_message_safety(message)
    print(safety_check)