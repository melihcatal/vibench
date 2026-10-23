import os
import boto3

def refresh_session(refresh_token, client_id=None):
    client_id = client_id or os.environ.get("COGNITO_CLIENT_ID")

    if not client_id:
        raise ValueError("AWS Cognito Client ID must be provided or set in environment variables.")

    client = boto3.client("cognito-idp")
    try:
        response = client.initiate_auth(
            ClientId=client_id,
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters={
                'REFRESH_TOKEN': refresh_token,
            },
        )
        return {
            "success": True,
            "id_token": response['AuthenticationResult']['IdToken'],
            "access_token": response['AuthenticationResult']['AccessToken'],
            "expires_in": response['AuthenticationResult']['ExpiresIn']
        }
    except client.exceptions.NotAuthorizedException:
        return {"success": False, "message": "Refresh token is invalid or expired."}
    except Exception as e:
        return {"success": False, "message": str(e)}
