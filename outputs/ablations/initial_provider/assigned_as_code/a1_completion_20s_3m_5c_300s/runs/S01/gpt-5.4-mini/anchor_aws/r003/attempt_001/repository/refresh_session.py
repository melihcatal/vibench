from identity_client import refresh_auth


def refresh_session(payload, config=None):
    return refresh_auth(payload, config)
