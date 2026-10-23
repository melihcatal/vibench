import urllib.parse

import boto3

from identity_client import build_login_request, load_identity_config


def start_oauth_login() -> str:
    cfg = load_identity_config()
    req = build_login_request()
    cognito = boto3.client("cognito-idp", region_name=cfg["aws_region"])
    _ = cognito.describe_user_pool_client(UserPoolId=os.environ.get("COGNITO_USER_POOL_ID", ""), ClientId=req.client_id)
    params = {
        "response_type": "code",
        "client_id": req.client_id,
        "redirect_uri": req.redirect_uri,
        "scope": req.scope,
        "state": req.state,
    }
    authorize_url = f"https://{cfg['cognito_domain']}/oauth2/authorize?{urllib.parse.urlencode(params)}"
    return authorize_url
