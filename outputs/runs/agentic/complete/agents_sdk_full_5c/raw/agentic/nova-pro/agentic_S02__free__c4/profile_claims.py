import google.auth.transport.requests
import google.oauth2.id_token

def fetch_profile_claims(id_token):
    requests_session = google.auth.transport.requests.Request()
    id_info = google.oauth2.id_token.verify_oauth2_token(
        id_token, requests_session, 'your-client-id')
    return id_info