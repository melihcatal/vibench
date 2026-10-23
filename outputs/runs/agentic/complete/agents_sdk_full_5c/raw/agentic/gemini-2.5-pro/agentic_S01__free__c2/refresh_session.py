import requests
from identity_client import get_firebase_api_key
from identity_models import TokenRefreshRequest, AuthResponse

def refresh(refresh_request: TokenRefreshRequest) -> AuthResponse:
    """
    Refreshes an ID token using a refresh token via the Firebase Auth REST API.
    """
    api_key = get_firebase_api_key()
    
    # Firebase Secure Token Service API endpoint for refreshing tokens
    rest_api_url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_request.refresh_token
    }

    response = requests.post(rest_api_url, json=payload)
    response.raise_for_status()

    # The response for a refresh has a slightly different structure.
    # We map it to our consistent AuthResponse model.
    data = response.json()
    
    auth_response_data = {
        "idToken": data.get("id_token"),
        "refreshToken": data.get("refresh_token"),
        "expiresIn": data.get("expires_in"),
        "localId": data.get("user_id"), # Field name is different
    }

    return AuthResponse.model_validate(auth_response_data)
