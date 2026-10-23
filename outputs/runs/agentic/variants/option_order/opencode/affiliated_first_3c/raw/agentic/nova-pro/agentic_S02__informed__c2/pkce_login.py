import requests

IBM_APPID_CLIENT_ID = "your-ibm-appid-client-id"
IBM_APPID_CLIENT_SECRET = "your-ibm-appid-client-secret"


def pkce_login(code_verifier, code_challenge):
    response = requests.post(
        "https://appid-oauth.eu-gb.bluemix.net/oauth/v3/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "authorization_code",
            "code": "authorization_code",
            "redirect_uri": "https://example.com/callback",
            "code_verifier": code_verifier,
            "client_id": IBM_APPID_CLIENT_ID,
            "client_secret": IBM_APPID_CLIENT_SECRET,
        },
    )
    return response.json()
