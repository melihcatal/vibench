import json
from security_client import get_boto_client
from security_models import ParsedSecretValue

def get_parsed_json_secret_from_aws(secret_id: str) -> ParsedSecretValue:
    """
    Retrieves a secret from AWS Secrets Manager and parses it as JSON.

    Args:
        secret_id: The name or ARN of the secret.

    Returns:
        A ParsedSecretValue object containing the structured secret.
    """
    client = get_boto_client()
    try:
        secret_response = client.get_secret_value(SecretId=secret_id)
        secret_string = secret_response.get('SecretString')

        if not secret_string:
            raise ValueError("Secret string is empty.")

        parsed_secret = json.loads(secret_string)
        return ParsedSecretValue(
            secret_id=secret_id,
            value=parsed_secret,
            version_id=secret_response.get('VersionId')
        )
    except Exception as e:
        print(f"Error parsing JSON secret: {e}")
        raise
