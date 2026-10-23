from identity_client import GOOGLE_AUTH_URL, GOOGLE_CLIENT_ID


def start_oauth_login():
    auth_url = f"{GOOGLE_AUTH_URL}?client_id={GOOGLE_CLIENT_ID}&response_type=code&scope=openid+profile+email&redirect_uri=http://localhost:8000/oauth_callback"
    print(f"Redirect to: {auth_url}")
    return auth_url
