import os
from identity_client import CognitoClient
from identity_models import PasswordResetRequest


def password_reset(payload: PasswordResetRequest, config=None) -> dict:
    config = config or {}
    cognito_client = CognitoClient(
        region_name=config.get("region"),
        client_id=config.get("client_id"),
        client_secret=config.get("client_secret")
    )

    # For password reset, we first need to forgot password
    # Cognito will send a confirmation code to the user's email
    try:
        response = cognito_client.client.forgot_password(
            ClientId=cognito_client.client_id,
            Username=payload.email,
            SecretHash=cognito_client._get_secret_hash(payload.email) # SecretHash is needed if client has one
        )
        return {"status": "PASSWORD_RESET_INITIATED", "code_delivery_details": response.get('CodeDeliveryDetails')}
    except cognito_client.client.exceptions.UserNotFoundException:
        return {"status": "USER_NOT_FOUND", "message": "User not found."}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}
