from urllib.parse import urlparse, parse_qs
from google_auth_oauthlib.flow import InstalledAppFlow
from identity_client import get_google_client_config, SCOPES, REDIRECT_URI
from identity_models import Tokens


def handle_oauth_callback(callback_url: str, flow: InstalledAppFlow):
    query_params = parse_qs(urlparse(callback_url).query)
    code = query_params.get("code", [None])[0]
    if not code:
        raise ValueError("No authorization code in callback")
    flow.fetch_token(code=code)
    creds = flow.credentials
    return Tokens(
        access_token=creds.token,
        id_token=creds.id_token,
        refresh_token=creds.refresh_token,
    )
