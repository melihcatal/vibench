from __future__ import annotations

from identity_client import build_authorize_request, generate_nonce, generate_state, load_identity_config


def start_oauth_login() -> str:
    config = load_identity_config()
    state = generate_state()
    nonce = generate_nonce()
    return build_authorize_request(config, ["openid", "profile", "email"], state, nonce=nonce)


if __name__ == "__main__":
    print(start_oauth_login())
