from identity_client import COGNITO_PROVIDER, get_cognito_client, get_cognito_client_id
from identity_models import RegisterUserRequest, RegisterUserResponse


def register_user(email: str, password: str, display_name: str | None = None) -> dict:
    request = RegisterUserRequest(
        email=email, password=password, display_name=display_name
    )
    client = get_cognito_client()
    response = client.sign_up(
        ClientId=get_cognito_client_id(),
        Username=request.email,
        Password=request.password,
        UserAttributes=request.to_cognito_attributes(),
    )
    delivery = response.get("CodeDeliveryDetails") or {}
    result = RegisterUserResponse(
        provider=COGNITO_PROVIDER,
        user_sub=response.get("UserSub"),
        user_confirmed=bool(response.get("UserConfirmed")),
        delivery_destination=delivery.get("Destination"),
        delivery_medium=delivery.get("DeliveryMedium"),
        message="User registered with Amazon Cognito User Pools",
    )
    return result.to_dict()
