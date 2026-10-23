import requests

from identity_client import merge_payload


def oauth_callback(payload, config=None):
    data = merge_payload(payload, config)
    request = {"code": data["code"], "returnSecureToken": True}
    if data.get("redirect_uri"):
        request["redirectUri"] = data["redirect_uri"]
    response = requests.post("https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp",
                             params={"key": data["api_key"]}, json=request, timeout=30)
    response.raise_for_status()
    result = response.json()
    return {
        "access_token": result.get("oauthAccessToken") or result.get("idToken"),
        "refresh_token": result.get("refreshToken"),
        "id_token": result.get("idToken"),
        "user_id": result.get("localId"),
    }
