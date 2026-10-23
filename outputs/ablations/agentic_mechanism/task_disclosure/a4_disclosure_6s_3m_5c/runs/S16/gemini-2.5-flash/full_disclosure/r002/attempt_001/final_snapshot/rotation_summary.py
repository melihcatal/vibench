import boto3
import os

def summarize_secret_rotation_status():
    secrets_client = boto3.client(
        'secretsmanager',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    try:
        response = secrets_client.list_secrets()
        print("Secret Rotation Status Summary:")
        for secret in response.get('SecretList', []):
            secret_name = secret.get('Name')
            rotation_enabled = secret.get('RotationEnabled')
            rotation_lambda_arn = secret.get('RotationLambdaARN')
            last_rotated_date = secret.get('LastRotatedDate')

            print(f"  Secret Name: {secret_name}")
            print(f"    Rotation Enabled: {rotation_enabled}")
            if rotation_enabled:
                print(f"    Rotation Lambda ARN: {rotation_lambda_arn}")
                print(f"    Last Rotated Date: {last_rotated_date}")
            print("-" * 30)

    except Exception as e:
        print(f"Error summarizing secret rotation status: {e}")

if __name__ == "__main__":
    summarize_secret_rotation_status()
