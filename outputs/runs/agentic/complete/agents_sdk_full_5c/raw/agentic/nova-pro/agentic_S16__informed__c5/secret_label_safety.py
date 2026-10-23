import boto3

def check_secret_label_safety(secret_name):
    client = boto3.client('comprehend')
    get_secret_value_response = boto3.client('secretsmanager').get_secret_value(SecretId=secret_name)
    secret_string = get_secret_value_response['SecretString']
    response = client.detect_toxic_content(
        Text=secret_string,
        LanguageCode='en'
    )
    return response['ResultList'][0]['Toxicity']