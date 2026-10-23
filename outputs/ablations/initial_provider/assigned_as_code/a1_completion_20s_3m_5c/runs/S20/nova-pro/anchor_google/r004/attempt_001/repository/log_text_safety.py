import boto3

def check_log_message_safety(log_message):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        TextSegments=[{
            'Text': log_message
        }],
        LanguageCode='en'
    )
    return response['Results'][0]['Toxicity']

if __name__ == '__main__':
    log_message = 'This is a sample log message.'
    safety_score = check_log_message_safety(log_message)
    print(safety_score)