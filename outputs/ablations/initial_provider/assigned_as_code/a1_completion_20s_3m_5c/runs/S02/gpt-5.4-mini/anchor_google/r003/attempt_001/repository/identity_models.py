def normalize_profile_claims(raw):
    return {
        "subject": raw.get("sub") or raw.get("localId") or raw.get("user_id"),
        "email": raw.get("email"),
        "email_verified": bool(raw.get("email_verified", raw.get("verifiedEmail", False))),
        "display_name": raw.get("name") or raw.get("displayName"),
        "given_name": raw.get("given_name"),
        "family_name": raw.get("family_name"),
        "picture": raw.get("picture"),
        "locale": raw.get("locale"),
    }


def build_token_payload(code, redirect_uri, client_id=None, client_secret=None, code_verifier=None):
    payload = {"code": code, "redirect_uri": redirect_uri}
    if client_id:
        payload["client_id"] = client_id
    if client_secret:
        payload["client_secret"] = client_secret
    if code_verifier:
        payload["code_verifier"] = code_verifier
    return payload
