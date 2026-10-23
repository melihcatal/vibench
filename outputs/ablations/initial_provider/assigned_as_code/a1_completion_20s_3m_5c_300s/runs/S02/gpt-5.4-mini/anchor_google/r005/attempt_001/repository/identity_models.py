def normalize_profile_claims(claims):
    claims = dict(claims or {})
    emails = claims.get("emails") or []
    primary_email = claims.get("email") or (emails[0] if emails else None)
    return {
        "subject": claims.get("sub") or claims.get("user_id"),
        "email": primary_email,
        "display_name": claims.get("name") or claims.get("displayName"),
        "given_name": claims.get("given_name"),
        "family_name": claims.get("family_name"),
        "picture": claims.get("picture") or claims.get("photoUrl"),
        "raw": claims,
    }


def normalize_audit_record(event):
    event = dict(event or {})
    return {
        "actor": event.get("actor") or event.get("sub"),
        "action": event.get("action"),
        "status": event.get("status"),
        "timestamp": event.get("timestamp") or event.get("time"),
        "details": event,
    }
