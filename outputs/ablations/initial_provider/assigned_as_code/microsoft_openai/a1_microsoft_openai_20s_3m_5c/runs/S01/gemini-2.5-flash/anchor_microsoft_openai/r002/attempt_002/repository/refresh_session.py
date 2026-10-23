from identity_client import IdentityClient
from identity_models import TokenRefreshPayload, AuthTokens

def refresh_session(payload: TokenRefreshPayload, identity_client: IdentityClient):
    msal_app = identity_client.get_msal_app()
    
    # MSAL's acquire_token_by_refresh_token requires a list of scopes.
    # The scopes should be the same ones for which the original access token was issued.
    # For this example, we'll use common scopes that would typically allow token refresh.
    scopes = ["User.Read", "openid", "profile", "offline_access"]
    
    result = msal_app.acquire_token_by_refresh_token(
        refresh_token=payload.refresh_token,
        scopes=scopes
    )

    if "access_token" in result:
        return AuthTokens(
            access_token=result["access_token"],
            refresh_token=result.get("refresh_token"),  # Refresh token might be renewed
            expires_in=result.get("expires_in")
        )
    else:
        raise RuntimeError(f"Token refresh failed: {result.get("error_description", result.get("error"))}")
