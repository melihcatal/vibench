import boto3


def email_password_login(email, password):
    client = boto3.client("cognito-idp", region_name="us-west-2")
    response = client.initiate_auth(
        ClientId="your_client_id",
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": email, "PASSWORD": password},
    )
    return response
