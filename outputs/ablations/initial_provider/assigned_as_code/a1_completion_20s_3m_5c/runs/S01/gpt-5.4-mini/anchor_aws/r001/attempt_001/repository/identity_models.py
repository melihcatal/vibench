def normalize_email_password_payload(payload):
    payload = dict(payload or {})
    if "email" in payload:
        payload["email"] = payload["email"].strip().lower()
    return payload


def wrap_result(**kwargs):
    return kwargs
