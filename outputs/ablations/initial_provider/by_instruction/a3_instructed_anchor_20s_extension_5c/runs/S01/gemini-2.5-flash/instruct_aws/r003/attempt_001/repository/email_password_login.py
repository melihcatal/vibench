import os
import boto3

def email_password_login(email, password, user_pool_id=None, client_id=None):
    user_pool_id = user_pool_id or os.environ.get("COGNITO_USER_POOL_ID")
    client_id = client_id or os.environ.get("COGNITO_CLIENT_ID")

    if not user_pool_id or not client_id:
        raise ValueError("AWS Cognito User Pool ID and Client ID must be provided or set in environment variables.")

    client = boto3.client("cognito-idp")
    try:
        response = client.initiate_auth(
            ClientId=client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password,
            },
        )
        return {
            "success": True,
            "id_token": response['AuthenticationResult']['IdToken'],
            "access_token": response['AuthenticationResult']['AccessToken'],
            "refresh_token": response['AuthenticationResult']['RefreshToken'],
            "expires_in": response['AuthenticationResult']['ExpiresIn']
        }
    except client.exceptions.NotAuthorizedException:
        return {"success": False, "message": "Incorrect username or password."}
    except client.exceptions.UserNotFoundException:
        return {"success": False, "message": "User not found."}
    except Exception as e:
        return {"success": False, "message": str(e)}
