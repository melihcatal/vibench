import boto3
import os

def refresh_session(refresh_token, client_id):
    """
    Refreshes an expired session or access token using AWS Cognito.
    """
    try:
        cognito_idp_client = boto3.client('cognito-idp', region_name=os.environ.get("AWS_REGION"))

        response = cognito_idp_client.initiate_auth(
            ClientId=client_id,
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters={
                'REFRESH_TOKEN': refresh_token
            }
        )

        return {
            "success": True,
            "message": "Session refreshed successfully.",
            "AuthenticationResult": response.get('AuthenticationResult')
        }
    except Exception as e:
        return {"success": False, "message": str(e)}
