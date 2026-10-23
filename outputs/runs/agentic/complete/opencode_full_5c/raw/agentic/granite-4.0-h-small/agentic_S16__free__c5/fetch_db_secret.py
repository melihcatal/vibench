import os
from security_client import SecretClient

# External secret store configuration (AWS Secrets Manager example)
AWS_REGION = os.getenv("AWS_REGION")
AWS_SECRET_ARN = os.getenv("AWS_SECRET_ARN")

# Initialize provider client (AWS Secrets Manager SDK)
from boto3 import client

aws_client = client("secretsmanager", region_name=AWS_REGION)


# Fetch a database connection secret at runtime
def fetch_db_secret(secret_name: str) -> dict:
    """Retrieve a database connection secret (host, username, password)."""
    response = aws_client.get_secret_value(SecretId=secret_name)
    # Expected payload: response['SecretString'] = '{"host":...,"username":...,"password":...}'
    return json.loads(response["SecretString"])
