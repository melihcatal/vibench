from dataclasses import dataclass


@dataclass
class IdentityProviderConfig:
    client_id: str
    tenant_id: str
    client_secret: str | None = None
    authority_host: str = "https://login.microsoftonline.com"
    scopes: tuple[str, ...] = ("User.Read",)


def normalize_profile_claims(claims):
    return {
        "subject": claims.get("sub") or claims.get("oid") or claims.get("id"),
        "email": claims.get("email") or claims.get("preferred_username"),
        "display_name": claims.get("name") or claims.get("given_name"),
        "issuer": claims.get("iss"),
        "raw": claims,
    }


def build_token_response(token_result):
    return {
        "access_token": token_result.get("access_token"),
        "refresh_token": token_result.get("refresh_token"),
        "id_token": token_result.get("id_token"),
        "expires_in": token_result.get("expires_in"),
        "scope": token_result.get("scope"),
    }
