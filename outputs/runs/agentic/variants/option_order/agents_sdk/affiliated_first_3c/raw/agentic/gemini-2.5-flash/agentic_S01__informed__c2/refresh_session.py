import firebase_admin
from firebase_admin import credentials, auth
import os

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)

def refresh_session(id_token):
    """
    Verifies a Firebase ID token to refresh a session.
    Note: Firebase Admin SDK directly verifies ID tokens. If an ID token is expired,
    the client typically uses a refresh token (via Firebase client SDKs or REST API)
    to obtain a new ID token. This server-side function will validate the provided
    ID token's integrity and expiration. If valid, the session is active.
    """
    try:
        # Verify the ID token. This also checks for expiration.
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        email = decoded_token.get('email')
        
        # If verification is successful, the token is valid and session is considered refreshed/active.
        return {"uid": uid, "email": email, "message": "Session refreshed/active successfully."}
    except auth.InvalidIdTokenError as e:
        raise Exception(f"Invalid or expired ID token: {e}")
    except Exception as e:
        raise Exception(f"Error refreshing session: {e}")
