import boto3


def register_user(email, password):
    cognito_client = boto3.client("cognito-idp")
    response = cognito_client.sign_up(
        ClientId="YOUR_COGNITO_CLIENT_ID",
        Username=email,
        Password=password,
        UserAttributes=[{"Name": "email", "Value": email}],
    )
    return response
