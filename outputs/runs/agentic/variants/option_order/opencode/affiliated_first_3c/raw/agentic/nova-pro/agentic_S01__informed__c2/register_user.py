import boto3


def register_user(email, password):
    client = boto3.client("cognito-idp", region_name="us-east-1")
    response = client.sign_up(
        ClientId="your-client-id",
        Username=email,
        Password=password,
        UserAttributes=[{"Name": "email", "Value": email}],
    )
    return response
