import os
import boto3

def password_reset(email, user_pool_id=None, client_id=None):
    user_pool_id = user_pool_id or os.environ.get("COGNITO_USER_POOL_ID")
    client_id = client_id or os.environ.get("COGNITO_CLIENT_ID")

    if not user_pool_id or not client_id:
        raise ValueError("AWS Cognito User Pool ID and Client ID must be provided or set in environment variables.")

    client = boto3.client("cognito-idp")
    try:
        response = client.forgot_password(
            ClientId=client_id,
            Username=email,
            SecretHash="",
        )
        # Cognito sends a confirmation code to the user's email or phone
        return {"success": True, "message": "Password reset initiated. Check your email for a verification code."}
    except client.exceptions.UserNotFoundException:
        return {"success": False, "message": "User not found."}
    except Exception as e:
        return {"success": False, "message": str(e)}
