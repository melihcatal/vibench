import webbrowser
import uuid
from datetime import datetime
from identity_client import IdentityClient
from identity_models import AuditEvent


def start_oauth_login(state: str = None, ip_address: str = "127.0.0.1"):
    client = IdentityClient()
    auth_url = client.build_auth_url(state)
    print(f"Opening Auth0 OAuth login URL: {auth_url}")
    webbrowser.open(auth_url)
    audit_id = str(uuid.uuid4())
    audit = AuditEvent(
        id=audit_id,
        timestamp=datetime.now().isoformat(),
        event_type="login_start",
        client_id=client.config.client_id,
        ip_address=ip_address,
    )
    print(f"Audit event logged: {audit}")
    return auth_url, audit


if __name__ == "__main__":
    start_oauth_login()
