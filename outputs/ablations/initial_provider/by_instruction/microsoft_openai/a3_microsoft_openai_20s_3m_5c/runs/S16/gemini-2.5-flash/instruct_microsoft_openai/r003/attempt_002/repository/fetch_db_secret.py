import boto3
import os

def fetch_db_secret(secret_name: str) -> str:
    """
    Fetches a database connection secret from AWS Secrets Manager.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    client = boto3.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        else:
            # Handle binary secrets if necessary, though for DB secrets, string is common.
            raise ValueError("SecretString not found in the response, binary secrets are not handled.")
    except Exception as e:
        raise RuntimeError(f"Could not retrieve secret {secret_name} from AWS Secrets Manager: {e}")

