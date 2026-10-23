from identity_client import FirebaseAuthClient
from identity_models import UserLoginRequest, AuthTokenResponse


def login_user_with_password(login_details: UserLoginRequest) -> AuthTokenResponse:
    """
    Signs in a user with email and password using Firebase Auth REST API.
    """
    client = FirebaseAuthClient()
    try:
        response_data = client.sign_in_with_password(
            login_details.email, login_details.password
        )
        return AuthTokenResponse(
            id_token=response_data.get("idToken"),
            refresh_token=response_data.get("refreshToken"),
            expires_in=int(response_data.get("expiresIn")),
            local_id=response_data.get("localId"),
        )
    except Exception as e:
        # Proper error handling should be implemented
        raise Exception(f"Login failed: {str(e)}")
