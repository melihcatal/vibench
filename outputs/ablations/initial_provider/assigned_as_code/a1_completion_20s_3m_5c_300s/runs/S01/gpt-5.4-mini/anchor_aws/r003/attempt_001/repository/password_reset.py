from identity_client import start_password_reset


def password_reset(payload, config=None):
    return start_password_reset(payload, config)
