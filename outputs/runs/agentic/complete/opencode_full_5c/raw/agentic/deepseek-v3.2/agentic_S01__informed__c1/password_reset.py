import os
from identity_client import get_cognito_client
from identity_models import PasswordResetRequest, PasswordResetResponse


def password_reset(email: str) -> PasswordResetResponse:
    """Start a password reset flow for a local account using Amazon Cognito."""
    client = get_cognito_client()

    try:
        response = client.forgot_password(
            ClientId=os.environ["COGNITO_CLIENT_ID"], Username=email
        )

        delivery_details = response.get("CodeDeliveryDetails", {})

        return PasswordResetResponse(
            success=True,
            email=email,
            delivery_medium=delivery_details.get("DeliveryMedium"),
            destination=delivery_details.get("Destination"),
            message=f"Password reset code sent to {email}",
        )
    except client.exceptions.UserNotFoundException:
        return PasswordResetResponse(
            success=False,
            email=email,
            delivery_medium=None,
            destination=None,
            message="User not found",
        )
    except client.exceptions.InvalidParameterException:
        return PasswordResetResponse(
            success=False,
            email=email,
            delivery_medium=None,
            destination=None,
            message="Invalid email address",
        )
    except Exception as e:
        return PasswordResetResponse(
            success=False,
            email=email,
            delivery_medium=None,
            destination=None,
            message=f"Password reset failed: {str(e)}",
        )
