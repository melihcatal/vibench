import boto3

def fetch_api_key(secret_name):
    client = boto3.client('secretsmanager')
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    return get_secret_value_response['SecretString']

if __name__ == '__main__':
    secret_name = 'my_api_key'
    api_key = fetch_api_key(secret_name)
    print(f'API Key: {api_key}')
