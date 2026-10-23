import boto3
import os

def fetch_db_secret(secret_name: str) -> str:
    """
    Fetches a database connection secret from AWS Secrets Manager.
    """
    region_name = os.getenv("AWS_REGION", "us-east-1")
    client = boto3.client("secretsmanager", region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    if "SecretString" in response:
        return response["SecretString"]
    else:
        return response["SecretBinary"].decode("utf-8")

if __name__ == "__main__":
    # Example usage:
    # secret_name = "my-db-secret"
    # db_secret = fetch_db_secret(secret_name)
    # print(f"Fetched DB Secret: {db_secret}")
    pass
