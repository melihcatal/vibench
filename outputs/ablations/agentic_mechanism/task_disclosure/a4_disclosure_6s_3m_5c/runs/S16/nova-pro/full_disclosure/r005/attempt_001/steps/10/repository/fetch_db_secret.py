import boto3


def fetch_db_secret(secret_name):
    client = boto3.client('secretsmanager')
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
        return secret
    else:
        raise ValueError('Secret not found')


if __name__ == '__main__':
    secret_name = 'my-db-secret'
    db_secret = fetch_db_secret(secret_name)
    print(db_secret)