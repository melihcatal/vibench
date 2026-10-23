from auth0 import Auth0


def email_password_login(email, password):
    auth0 = Auth0(domain="your_auth0_domain", client_id="your_client_id")
    tokens = auth0.password.login(email, password)
    return tokens
