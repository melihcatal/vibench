from identity_client import exchange_code_for_token
from identity_models import TokenResponse


def handle_callback(code: str, code_verifier: str = None) -> TokenResponse:
    tokens = exchange_code_for_token(code, code_verifier=code_verifier)
    return TokenResponse(
        access_token=tokens.get("access_token", ""),
        id_token=tokens.get("id_token", ""),
        refresh_token=tokens.get("refresh_token", ""),
        token_type=tokens.get("token_type", "Bearer"),
        expires_in=int(tokens.get("expires_in", 0)),
    )
