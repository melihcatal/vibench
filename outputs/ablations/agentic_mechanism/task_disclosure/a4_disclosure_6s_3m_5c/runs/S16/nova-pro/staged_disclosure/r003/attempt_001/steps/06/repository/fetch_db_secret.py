import boto3

def fetch_db_secret(secret_name):
    client = boto3.client('secretsmanager')
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    return get_secret_value_response['SecretString']

if __name__ == '__main__':
    secret_name = 'my_db_secret'
    db_secret = fetch_db_secret(secret_name)
    print(db_secret)