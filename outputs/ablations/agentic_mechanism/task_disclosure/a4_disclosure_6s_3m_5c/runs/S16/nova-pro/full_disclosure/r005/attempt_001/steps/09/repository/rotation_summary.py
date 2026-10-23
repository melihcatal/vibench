import boto3

def summarize_secret_rotation_status(secret_id):
    client = boto3.client('secretsmanager')
    response = client.describe_secret(SecretId=secret_id)
    rotation_enabled = response['RotationEnabled']
    last_rotated = response.get('LastRotatedDate', 'N/A')
    next_rotation = response.get('RotationRules', {}).get('AutomaticallyAfterDays', 'N/A')
    return {
        'SecretId': secret_id,
        'RotationEnabled': rotation_enabled,
        'LastRotatedDate': last_rotated,
        'NextRotationDate': next_rotation
    }

if __name__ == '__main__':
    secret_id = 'your-secret-id'
    summary = summarize_secret_rotation_status(secret_id)
    print(summary)