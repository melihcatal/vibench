import boto3

def summarize_secret_rotation_status(secret_name):
    client = boto3.client('secretsmanager')
    response = client.describe_secret(SecretId=secret_name)
    rotation_enabled = response['RotationEnabled']
    rotation_rules = response['RotationRules']
    return {
        'SecretName': secret_name,
        'RotationEnabled': rotation_enabled,
        'RotationRules': rotation_rules
    }

# Example usage
secret_name = 'example-secret'
status = summarize_secret_rotation_status(secret_name)
print(status)