import boto3

def start_password_reset(username):
    client = boto3.client('cognito-idp', region_name='us-west-2')
    response = client.forgot_password(
        ClientId='your_client_id',
        Username=username
    )
    print(response)

if __name__ == '__main__':\n    username = input('Enter your username: ')
    start_password_reset(username)