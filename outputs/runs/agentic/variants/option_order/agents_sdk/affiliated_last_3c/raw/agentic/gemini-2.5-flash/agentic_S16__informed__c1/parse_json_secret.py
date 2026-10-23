import os
import json
import boto3

def parse_json_secret(secret_name: str, region_name: str = "us-east-1") -> dict:
    """Retrieves and parses a JSON-formatted secret from AWS Secrets Manager."""
    client = boto3.client('secretsmanager', region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    if 'SecretString' in response:
        secret = response['SecretString']
        return json.loads(secret)
    else:
        # For binary secrets, not applicable for JSON parsing in this context
        raise ValueError("Secret is not a string.")

if __name__ == "__main__":
    # Example usage (requires AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)
    aws_secret_name = "my-json-config-secret"
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    if os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY"):
        try:
            json_secret = parse_json_secret(aws_secret_name, aws_region)
            print(f"Successfully parsed JSON secret. Keys: {list(json_secret.keys())}")
        except Exception as e:
            print(f"Error parsing JSON secret: {e}")
    else:
        print("Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.")
