import hashlib
import base64

from identity_client import authorization_url, build_pkce_request


def pkce_login() -> dict:
    request = build_pkce_request()
    challenge = request.state.split(":", 1)[1]
    return {
        "authorization_url": authorization_url(request, challenge),
        "code_verifier": request.code_verifier,
        "state": request.state,
    }
