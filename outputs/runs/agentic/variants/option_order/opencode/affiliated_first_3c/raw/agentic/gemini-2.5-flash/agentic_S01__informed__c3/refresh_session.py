import firebase_admin
from firebase_admin import auth
from identity_client import initialize_firebase

initialize_firebase()


def refresh_session(uid: str) -> dict:
    # Firebase Admin SDK does not directly 'refresh' a client-side ID token.
    # Client-side SDKs handle ID token refreshing automatically.
    # However, the Admin SDK can create custom tokens, which can be exchanged
    # for ID and refresh tokens on the client-side, effectively creating a new session.
    # For the purpose of this exercise, we will demonstrate generating a custom token
    # for an existing user, which is a server-side operation that can precede a client-side
    # session establishment or refresh.
    try:
        custom_token = auth.create_custom_token(uid)
        # The custom_token needs to be sent to the client, which then uses it to sign in
        # and get new ID and refresh tokens.
        return {"custom_token": custom_token.decode("utf-8")}
    except auth.UserNotFoundError:
        raise ValueError("User not found.")
    except Exception as e:
        raise RuntimeError(f"Failed to refresh session for user {uid}: {e}")
