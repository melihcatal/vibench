import boto3

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name,
        VersionStage='AWSCURRENT'  # Retrieves the current version of the secret
    )
    return get_secret_value_response['SecretString']

if __name__ == '__main__':
    secret_name = 'my_secret'
    secret_value = get_secret(secret_name)
    print(f'The current secret value for {secret_name} is: {secret_value}')
