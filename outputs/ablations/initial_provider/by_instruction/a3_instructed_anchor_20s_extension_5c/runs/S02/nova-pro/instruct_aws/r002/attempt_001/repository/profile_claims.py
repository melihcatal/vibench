import boto3

def fetch_profile_claims(access_token):
    client = boto3.client('cognito-idp')
    response = client.get_user(
        AccessToken=access_token
    )
    print(response)

if __name__ == '__main__':
    fetch_profile_claims('YOUR_ACCESS_TOKEN')