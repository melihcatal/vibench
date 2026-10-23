from identity_client import (
    build_authorization_url,
    generate_pkce_challenge,
    generate_pkce_verifier,
    generate_state,
)


def start_pkce_login() -> dict:
    verifier = generate_pkce_verifier()
    challenge = generate_pkce_challenge(verifier)
    state = generate_state()
    return {
        "authorization_url": build_authorization_url(
            state=state, code_challenge=challenge
        ),
        "state": state,
        "code_verifier": verifier,
        "code_challenge": challenge,
    }
