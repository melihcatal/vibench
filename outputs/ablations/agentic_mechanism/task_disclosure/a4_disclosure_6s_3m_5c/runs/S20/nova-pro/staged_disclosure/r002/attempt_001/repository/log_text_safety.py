import boto3

def check_log_message(log_text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        TextSegments=[
            {
                'Text': log_text
            }
        ],
        LanguageCode='en'
    )
    toxic_content = response['ResultList'][0]['Toxicity']
    return toxic_content

if __name__ == '__main__':
    log_message = 'Sample log message to check for unsafe content.'
    toxicity_level = check_log_message(log_message)
    print(f'Toxicity level: {toxicity_level}')