import boto3

def check_unsafe_content(log_message):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        Text=log_message,
        LanguageCode='en'
    )
    return response

if __name__ == '__main__':\n    log_message = 'Example log message to check for unsafe content.'
    result = check_unsafe_content(log_message)
    print(result)