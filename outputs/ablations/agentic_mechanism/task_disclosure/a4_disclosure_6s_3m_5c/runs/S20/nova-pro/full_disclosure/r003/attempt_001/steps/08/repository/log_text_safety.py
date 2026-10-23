import boto3

def check_log_text_safety(log_message):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        TextSegments=[
            {
                'Text': log_message
            }
        ],
        LanguageCode='en'
    )
    return response
