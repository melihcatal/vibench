import os
import json
from identity_client import get_identity_client
from identity_models import OAuthCallbackRequest, TokenResponse


def oauth_callback(callback_request: OAuthCallbackRequest):
    identity_client = get_identity_client()

    try:
        token_data = identity_client.exchange_code_for_tokens(
            code=callback_request.code,
            redirect_uri=callback_request.redirect_uri or identity_client.redirect_uri,
            code_verifier=callback_request.code_verifier
        )

        # Auth0 token response might vary, normalize it to TokenResponse
        token_response = TokenResponse(
            access_token=token_data.get("access_token"),
            id_token=token_data.get("id_token"),
            refresh_token=token_data.get("refresh_token"),
            expires_in=token_data.get("expires_in"),
            token_type=token_data.get("token_type", "Bearer"),
        )
        return {"status": "success", "token_response": token_response.__dict__}
    except Exception as e:
        return {"status": "error", "message": str(e)}

