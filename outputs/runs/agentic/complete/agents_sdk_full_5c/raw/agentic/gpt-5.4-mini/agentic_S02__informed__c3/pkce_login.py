from __future__ import annotations

from identity_client import build_authorize_request, code_challenge_s256, generate_code_verifier, generate_nonce, generate_state, load_identity_config


def start_pkce_login() -> dict[str, str]:
    config = load_identity_config()
    verifier = generate_code_verifier()
    challenge = code_challenge_s256(verifier)
    state = generate_state()
    nonce = generate_nonce()
    url = build_authorize_request(config, ["openid", "profile", "email"], state, nonce=nonce, code_challenge=challenge)
    return {"authorization_url": url, "code_verifier": verifier, "state": state, "nonce": nonce}
