from identity_client import AUTH0_ISSUER, authorization_url, build_oauth_request


def start_oauth_login() -> dict:
    request = build_oauth_request()
    return {
        "issuer": AUTH0_ISSUER,
        "authorization_url": authorization_url(request),
        "state": request.state,
    }
