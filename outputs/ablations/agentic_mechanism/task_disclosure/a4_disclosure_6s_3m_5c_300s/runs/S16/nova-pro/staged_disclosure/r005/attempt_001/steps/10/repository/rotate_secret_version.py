import boto3

def get_secret_value(secret_name, version_stage):
    client = boto3.client('secretsmanager')
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name,
            VersionStage=version_stage
        )
        return get_secret_value_response['SecretString']
    except client.exceptions.ResourceNotFoundException as e:
        print(f"Error: {e}")
    except client.exceptions.InvalidParameterException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    secret_name = 'my-secret'
    version_stage = 'AWSCURRENT'
    secret_value = get_secret_value(secret_name, version_stage)
    print(secret_value)