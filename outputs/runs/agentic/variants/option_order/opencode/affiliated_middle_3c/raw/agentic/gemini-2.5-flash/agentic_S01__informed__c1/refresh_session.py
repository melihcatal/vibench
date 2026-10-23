import os
import identity_client
from identity_models import RefreshTokenRequest


def refresh_session(request: RefreshTokenRequest) -> dict:
    """
    Refreshes an expired session or access token using Auth0 Authentication API.
    """
    authentication_client = identity_client.get_authentication_client()
    try:
        token_response = authentication_client.refresh_token(
            client_id=request.client_id,
            client_secret=request.client_secret,
            refresh_token=request.refresh_token,
            audience=request.audience,
            scope=request.scope,
        )
        return {
            "access_token": token_response.get("access_token"),
            "id_token": token_response.get("id_token"),
            "expires_in": token_response.get("expires_in"),
        }
    except Exception as e:
        raise RuntimeError(f"Auth0 token refresh failed: {e}")


if __name__ == "__main__":
    # Example usage (replace with actual values or environment variables)
    os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN.auth0.com"
    os.environ["AUTH0_CLIENT_ID"] = (
        "YOUR_AUTH0_CLIENT_ID"  # Client ID used to obtain the refresh token
    )
    os.environ["AUTH0_CLIENT_SECRET"] = (
        "YOUR_AUTH0_CLIENT_SECRET"  # Client Secret if it's a confidential client
    )
    os.environ["AUTH0_AUDIENCE"] = "YOUR_API_AUDIENCE"
    os.environ["AUTH0_REFRESH_TOKEN"] = "YOUR_REFRESH_TOKEN"

    refresh_request = RefreshTokenRequest(
        refresh_token=os.environ["AUTH0_REFRESH_TOKEN"],
        client_id=os.environ["AUTH0_CLIENT_ID"],
        client_secret=os.environ["AUTH0_CLIENT_SECRET"],
        audience=os.environ["AUTH0_AUDIENCE"],
    )
    try:
        result = refresh_session(refresh_request)
        print(f"Session refreshed successfully: {result}")
    except RuntimeError as e:
        print(f"Error: {e}")
