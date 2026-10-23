import boto3

def summarize_secret_rotation_status():
    client = boto3.client('secretsmanager')
    response = client.list_secrets()
    for secret in response['SecretList']:
        print(f"Secret: {secret['Name']}, RotationEnabled: {secret['RotationEnabled']}")

if __name__ == '__main__':
    summarize_secret_rotation_status()