import boto3

def summarize_secret_rotation_status():
    """
    Summarizes the rotation status of secrets in AWS Secrets Manager.
    """
    client = boto3.client('secretsmanager')
    
    paginator = client.get_paginator('list_secrets')
    response_iterator = paginator.paginate()

    print("AWS Secrets Manager Rotation Summary:")
    print("------------------------------------")

    for page in response_iterator:
        for secret in page['SecretList']:
            secret_name = secret.get('Name', 'N/A')
            rotation_enabled = secret.get('RotationEnabled', False)
            last_rotated_date = secret.get('LastRotatedDate')

            status = "Enabled" if rotation_enabled else "Disabled"
            last_rotated = last_rotated_date.strftime('%Y-%m-%d %H:%M:%S UTC') if last_rotated_date else 'N/A'

            print(f"Secret Name: {secret_name}")
            print(f"  Rotation Status: {status}")
            print(f"  Last Rotated: {last_rotated}")
            print("-" * 36)

if __name__ == "__main__":
    summarize_secret_rotation_status()
