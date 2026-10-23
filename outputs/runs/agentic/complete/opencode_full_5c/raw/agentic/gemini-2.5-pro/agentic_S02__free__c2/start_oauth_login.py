import os
from authlib.integrations.flask_client import OAuth
from identity_client import get_identity_config


def start_okta_login_flow(request):
    """
    Starts the OAuth 2.0 Authorization Code flow with Okta.
    """
    config = get_identity_config()
    oauth = OAuth(request.app)

    oauth.register(
        name="okta",
        client_id=config["okta_client_id"],
        client_secret=config["okta_client_secret"],
        server_metadata_url=f"https://{config['okta_domain']}/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

    redirect_uri = config["redirect_uri"]
    return oauth.okta.authorize_redirect(redirect_uri)


# This is a conceptual representation.
# A real implementation would require a web framework like Flask or Starlette.
