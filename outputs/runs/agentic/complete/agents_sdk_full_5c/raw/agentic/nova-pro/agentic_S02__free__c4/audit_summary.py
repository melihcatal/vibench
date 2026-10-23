import google.auth.transport.requests
import google.oauth2.id_token

def summarize_audit_events(id_token):
    requests_session = google.auth.transport.requests.Request()
    id_info = google.oauth2.id_token.verify_oauth2_token(
        id_token, requests_session, 'your-client-id')
    return id_info