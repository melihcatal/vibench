import os
from urllib.parse import urlencode


def get_auth0_config():
    return {
        "DOMAIN": os.getenv("AUTH0_DOMAIN"),
        "CLIENT_ID": os.getenv("AUTH0_CLIENT_ID"),
        "CLIENT_SECRET": os.getenv("AUTH0_CLIENT_SECRET"),
        "CALLBACK_URL": os.getenv("AUTH0_CALLBACK_URL"),
        "AUDIENCE": os.getenv("AUTH0_AUDIENCE"),
    }


def get_google_gemini_api_key():
    return os.getenv("GOOGLE_API_KEY")


def get_perspective_api_key():
    return os.getenv("PERSPECTIVE_API_KEY")


def get_google_cloud_credentials():
    return os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


def get_firestore_project_id():
    return os.getenv("GOOGLE_CLOUD_PROJECT")


def build_auth0_authorize_url(config, state, code_challenge=None):
    params = {
        "response_type": "code",
        "client_id": config["CLIENT_ID"],
        "redirect_uri": config["CALLBACK_URL"],
        "scope": "openid profile email",
        "state": state,
    }
    if config["AUDIENCE"]:
        params["audience"] = config["AUDIENCE"]
    if code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = "S256"
    return f"https://{config['DOMAIN']}/authorize?{urlencode(params)}"


def build_auth0_token_url(config):
    return f"https://{config['DOMAIN']}/oauth/token"


def build_auth0_userinfo_url(config):
    return f"https://{config['DOMAIN']}/userinfo"
