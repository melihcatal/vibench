import boto3


def email_password_login(username, password):
    client = boto3.client("cognito-idp", region_name="us-west-2")
    response = client.initiate_auth(
        ClientId="your-client-id",
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": username, "PASSWORD": password},
    )
    return response
