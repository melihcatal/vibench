import auth0

# Configuration
auth0_domain = "your-auth0-domain"
auth0_client_id = "your-auth0-client-id"
auth0_client_secret = "your-auth0-client-secret"
auth0_callback_url = "http://localhost:8000/callback"

# Auth0 client
auth0_client = auth0.Authentication(
    domain=auth0_domain,
    client_id=auth0_client_id,
    client_secret=auth0_client_secret,
    scope="openid profile email",
    audience="https://" + auth0_domain + "/userinfo",
)
