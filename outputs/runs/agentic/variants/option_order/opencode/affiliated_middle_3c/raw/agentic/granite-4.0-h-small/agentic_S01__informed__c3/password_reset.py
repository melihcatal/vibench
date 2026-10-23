import boto3

# Amazon Cognito User Pools integration
# Provider identifiable via boto3 client creation

cognito = boto3.client(
    "cognito-idp",
    aws_access_key_id="YOUR_AWS_ACCESS_KEY_ID",
    aws_secret_access_key="YOUR_AWS_SECRET_ACCESS_KEY",
    region_name="us-east-1",
)


def start_password_reset(email, user_pool_id, client_id):
    """Start a password reset flow for a local account.

    Args:
        email (str): User's email address.
        user_pool_id (str): The Cognito User Pool ID.
        client_id (str): App client ID in the user pool.

    Returns:
        dict: Response containing the challenge name and parameters if MFA is required,
              or confirmation if the reset code is sent.
    """
    response = cognito.forgot_password(ClientId=client_id, Username=email)
    return response


def confirm_password_reset(email, user_pool_id, client_id, reset_code, new_password):
    """Confirm the password reset code and set a new password.

    Args:
        email (str): User's email address.
        user_pool_id (str): The Cognito User Pool ID.
        client_id (str): App client ID in the user pool.
        reset_code (str): The verification code sent to the user.
        new_password (str): The new password to set.

    Returns:
        dict: Confirmation response from Cognito.
    """
    response = cognito.confirm_forgot_password(
        ClientId=client_id,
        Username=email,
        Password=new_password,
        ConfirmationCode=reset_code,
    )
    return response
