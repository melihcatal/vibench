import os
import boto3

def register_user(email, password, user_pool_id=None, client_id=None):
    user_pool_id = user_pool_id or os.environ.get("COGNITO_USER_POOL_ID")
    client_id = client_id or os.environ.get("COGNITO_CLIENT_ID")

    if not user_pool_id or not client_id:
        raise ValueError("AWS Cognito User Pool ID and Client ID must be provided or set in environment variables.")

    client = boto3.client("cognito-idp")
    try:
        response = client.sign_up(
            ClientId=client_id,
            SecretHash="",  # Not typically needed for public clients, or calculated client-side
            Username=email,
            Password=password,
            UserAttributes=[
                {"Name": "email", "Value": email},
            ],
        )
        return {"success": True, "user_sub": response["UserConfirmed"]}
    except client.exceptions.UsernameExistsException:
        return {"success": False, "message": "User with this email already exists."}
    except Exception as e:
        return {"success": False, "message": str(e)}
