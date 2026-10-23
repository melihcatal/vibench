from __future__ import annotations

from identity_client import get_supabase_client
from identity_models import RefreshSessionRequest, normalize_supabase_tokens


def refresh_session(request: RefreshSessionRequest):
    client = get_supabase_client()
    refreshed = client.auth.refresh_session(request.refresh_token)
    payload = {
        "access_token": refreshed.session.access_token,
        "refresh_token": refreshed.session.refresh_token,
        "token_type": refreshed.session.token_type,
        "expires_in": refreshed.session.expires_in,
        "id_token": getattr(refreshed.session, "id_token", None),
    }
    return normalize_supabase_tokens(payload)
