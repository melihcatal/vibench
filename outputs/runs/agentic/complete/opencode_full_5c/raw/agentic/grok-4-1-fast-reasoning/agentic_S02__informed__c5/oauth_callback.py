import os
import uuid
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from identity_client import IdentityClient
from identity_models import TokenResponse, UserProfile, AuditEvent


def handle_oauth_callback(full_url: str):
    parsed_url = urlparse(full_url)
    query_params = parse_qs(parsed_url.query)
    code = query_params.get("code", [None])[0]
    state = query_params.get("state", [None])[0]
    if not code:
        raise ValueError("No authorization code in callback")
    client = IdentityClient()
    tokens: TokenResponse = client.exchange_code(code)
    profile: UserProfile = client.get_user_profile(tokens.access_token)
    audit_id = str(uuid.uuid4())
    audit = AuditEvent(
        id=audit_id,
        timestamp=datetime.now().isoformat(),
        event_type="login_success",
        client_id=client.config.client_id,
        user_id=profile.sub,
        ip_address="127.0.0.1",
        success=True,
    )
    print(f"Login successful. Profile: {profile}")
    print(f"Audit event: {audit}")
    return tokens, profile, audit


if __name__ == "__main__":
    callback_url = os.getenv("CALLBACK_URL")
    if callback_url:
        handle_oauth_callback(callback_url)
