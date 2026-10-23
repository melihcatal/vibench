
import boto3

def get_secret_version(secret_name, version_id=None, version_stage=None):
    """
    Retrieves a specific version of a secret from AWS Secrets Manager.

    Args:
        secret_name (str): The name or Amazon Resource Name (ARN) of the secret.
        version_id (str, optional): The unique identifier of the secret version.
                                     If specified, the function returns the secret
                                     value for that version.
        version_stage (str, optional): The secret version stage that the secret
                                       version is Vended to. If specified, the
                                       function returns the secret value for the
                                       version with that stage.

    Returns:
        dict: A dictionary containing the secret string or binary, and other metadata.
              Returns None if the secret version is not found or an error occurs.
    """
    client = boto3.client('secretsmanager')
    try:
        if version_id:
            response = client.get_secret_value(SecretId=secret_name, VersionId=version_id)
        elif version_stage:
            response = client.get_secret_value(SecretId=secret_name, VersionStage=version_stage)
        else:
            # By default, get the current version
            response = client.get_secret_value(SecretId=secret_name)

        if 'SecretString' in response:
            return response['SecretString']
        else:
            return response['SecretBinary']
    except client.exceptions.ResourceNotFoundException:
        print(f"The secret '{secret_name}' or specified version/stage was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

