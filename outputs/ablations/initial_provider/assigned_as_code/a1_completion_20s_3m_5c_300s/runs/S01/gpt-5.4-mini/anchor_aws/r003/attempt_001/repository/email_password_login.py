from identity_client import sign_in


def email_password_login(payload, config=None):
    return sign_in(payload, config)
