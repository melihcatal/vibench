from identity_client import COGNITO_PROVIDER, get_cognito_client, get_cognito_client_id
from identity_models import PasswordResetRequest, PasswordResetResponse


def password_reset(email: str) -> dict:
    request = PasswordResetRequest(email=email)
    client = get_cognito_client()
    response = client.forgot_password(
        ClientId=get_cognito_client_id(), Username=request.email
    )
    delivery = response.get("CodeDeliveryDetails") or {}
    result = PasswordResetResponse(
        provider=COGNITO_PROVIDER,
        delivery_destination=delivery.get("Destination"),
        delivery_medium=delivery.get("DeliveryMedium"),
        message="Password reset initiated with Amazon Cognito User Pools",
    )
    return result.to_dict()
