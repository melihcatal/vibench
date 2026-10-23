import msal

from identity_models import IdentityProviderConfig


def load_identity_config(config):
    cfg = config or {}
    return IdentityProviderConfig(
        client_id=cfg["client_id"],
        tenant_id=cfg["tenant_id"],
        client_secret=cfg.get("client_secret"),
        authority_host=cfg.get("authority_host", "https://login.microsoftonline.com"),
        scopes=tuple(cfg.get("scopes", ["User.Read"])),
    )


def build_msal_app(config: IdentityProviderConfig):
    authority = f"{config.authority_host}/{config.tenant_id}"
    if config.client_secret:
        return msal.ConfidentialClientApplication(
            config.client_id,
            authority=authority,
            client_credential=config.client_secret,
        )
    return msal.PublicClientApplication(config.client_id, authority=authority)


def exchange_authorization_code(app, code, redirect_uri, scopes):
    return app.acquire_token_by_authorization_code(code, scopes=scopes, redirect_uri=redirect_uri)


def acquire_token_by_refresh_token(app, refresh_token, scopes):
    return app.acquire_token_by_refresh_token(refresh_token, scopes=scopes)
