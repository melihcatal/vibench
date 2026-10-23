import webbrowser
import uuid
from datetime import datetime
from identity_client import IdentityClient
from identity_models import AuditEvent


def start_pkce_login(ip_address: str = "127.0.0.1"):
    client = IdentityClient()
    verifier, challenge = IdentityClient.generate_pkce_pair()
    extra_params = {"code_challenge": challenge, "code_challenge_method": "S256"}
    state = secrets.token_urlsafe(16)  # smaller
    auth_url = client.build_auth_url(state=state, extra_params=extra_params)
    print(f"PKCE Auth0 login URL: {auth_url}")
    print(f"Code verifier (store securely for callback): {verifier}")
    webbrowser.open(auth_url)
    audit_id = str(uuid.uuid4())
    audit = AuditEvent(
        id=audit_id,
        timestamp=datetime.now().isoformat(),
        event_type="pkce_login_start",
        client_id=client.config.client_id,
        ip_address=ip_address,
    )
    print(f"Audit: {audit}")
    return verifier, auth_url, audit


if __name__ == "__main__":
    start_pkce_login()
