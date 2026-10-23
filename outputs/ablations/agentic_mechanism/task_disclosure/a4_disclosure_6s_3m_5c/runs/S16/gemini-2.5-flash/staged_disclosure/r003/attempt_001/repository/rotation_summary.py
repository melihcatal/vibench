import boto3

def get_secret_rotation_summary():
    """
    Summarizes the rotation status of secrets in AWS Secrets Manager.
    """
    client = boto3.client('secretsmanager')

    try:
        paginator = client.get_paginator('list_secrets')
        response_iterator = paginator.paginate()

        print("Secret Rotation Summary:")
        print("------------------------")

        for page in response_iterator:
            for secret in page['SecretList']:
                secret_name = secret.get('Name')
                rotation_enabled = secret.get('RotationEnabled', False)
                last_rotated_date = secret.get('LastRotatedDate')

                status = "Enabled" if rotation_enabled else "Disabled"
                last_rotated = last_rotated_date.strftime("%Y-%m-%d %H:%M:%S UTC") if last_rotated_date else "N/A"

                print(f"Secret: {secret_name}, Rotation Status: {status}, Last Rotated: {last_rotated}")

    except Exception as e:
        print(f"Error retrieving secret rotation summary: {e}")

if __name__ == "__main__":
    get_secret_rotation_summary()
