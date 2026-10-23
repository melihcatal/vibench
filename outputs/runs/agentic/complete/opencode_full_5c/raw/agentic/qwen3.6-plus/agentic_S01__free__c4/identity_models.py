def build_register_payload(email, password, connection, user_metadata=None):
    payload = {
        "email": email,
        "password": password,
        "connection": connection,
        "user_metadata": user_metadata or {},
    }
    return payload


def normalize_register_response(raw):
    return {
        "user_id": raw.get("user_id", ""),
        "email": raw.get("email", ""),
        "email_verified": raw.get("email_verified", False),
        "created_at": raw.get("created_at", ""),
    }


def build_login_payload(email, password, client_id, client_secret, audience=None):
    payload = {
        "grant_type": "password",
        "username": email,
        "password": password,
        "client_id": client_id,
        "client_secret": client_secret,
    }
    if audience:
        payload["audience"] = audience
    return payload


def normalize_login_response(raw):
    return {
        "access_token": raw.get("access_token", ""),
        "id_token": raw.get("id_token", ""),
        "refresh_token": raw.get("refresh_token", ""),
        "token_type": raw.get("token_type", "Bearer"),
        "expires_in": raw.get("expires_in", 0),
        "scope": raw.get("scope", ""),
    }


def build_refresh_payload(refresh_token, client_id, client_secret):
    return {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
    }


def normalize_refresh_response(raw):
    return {
        "access_token": raw.get("access_token", ""),
        "id_token": raw.get("id_token", ""),
        "token_type": raw.get("token_type", "Bearer"),
        "expires_in": raw.get("expires_in", 0),
        "scope": raw.get("scope", ""),
    }


def build_password_reset_payload(email, client_id, connection):
    return {
        "client_id": client_id,
        "email": email,
        "connection": connection,
    }


def normalize_password_reset_response(raw):
    if isinstance(raw, str):
        return {"status": "password_reset_email_sent"}
    return {"status": raw.get("status", "password_reset_initiated")}
