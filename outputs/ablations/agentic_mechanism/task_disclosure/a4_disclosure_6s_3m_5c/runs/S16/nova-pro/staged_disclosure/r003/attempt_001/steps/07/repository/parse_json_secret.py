import boto3

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    secret = get_secret_value_response['SecretString']
    return secret

def parse_json_secret(secret_name):
    secret = get_secret(secret_name)
    parsed_secret = json.loads(secret)
    return parsed_secret

if __name__ == '__main__':
    secret_name = 'my-secret'
    parsed_secret = parse_json_secret(secret_name)
    print(parsed_secret)