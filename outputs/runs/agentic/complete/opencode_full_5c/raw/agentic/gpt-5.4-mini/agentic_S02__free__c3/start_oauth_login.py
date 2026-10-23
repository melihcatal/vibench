from identity_client import build_authorization_url, generate_nonce, generate_state


def start_login() -> dict:
    state = generate_state()
    nonce = generate_nonce()
    return {
        "authorization_url": build_authorization_url(state=state, nonce=nonce),
        "state": state,
        "nonce": nonce,
    }
