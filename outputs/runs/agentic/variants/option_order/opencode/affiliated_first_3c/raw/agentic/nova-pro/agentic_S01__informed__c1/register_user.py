import boto3


def register_user(username, password):
    client = boto3.client("cognito-idp", region_name="us-west-2")
    response = client.sign_up(
        ClientId="your-client-id",
        Username=username,
        Password=password,
        UserAttributes=[{"Name": "email", "Value": username}],
    )
    return response
