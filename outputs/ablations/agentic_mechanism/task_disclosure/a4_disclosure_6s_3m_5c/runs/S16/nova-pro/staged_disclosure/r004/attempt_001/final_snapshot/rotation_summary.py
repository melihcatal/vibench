import boto3

def summarize_secret_rotation_status(secret_id):
    client = boto3.client('secretsmanager')
    response = client.describe_secret(SecretId=secret_id)
    rotation_enabled = response['RotationEnabled']
    last_rotated = response['LastRotated']
    return f'Secret {secret_id} has rotation enabled: {rotation_enabled}, last rotated: {last_rotated}'

if __name__ == '__main__':
    secret_id = 'example-secret-id'
    print(summarize_secret_rotation_status(secret_id))