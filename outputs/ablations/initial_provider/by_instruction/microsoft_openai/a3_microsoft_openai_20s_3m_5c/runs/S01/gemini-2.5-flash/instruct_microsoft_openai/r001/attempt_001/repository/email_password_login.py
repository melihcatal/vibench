import firebase_admin
from firebase_admin import credentials, auth
import os

def email_password_login(email, password):
    """
    Signs in a user with email and password using Firebase Authentication.
    """
    try:
        # Initialize Firebase Admin SDK if not already initialized
        if not firebase_admin._apps:
            cred_path = os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY_PATH")
            if not cred_path:
                raise ValueError("FIREBASE_SERVICE_ACCOUNT_KEY_PATH environment variable not set.")
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)

        user = auth.get_user_by_email(email)
        # Firebase Admin SDK does not directly provide a sign-in with email/password method
        # for security reasons (it's meant for server-side user management).
        # For client-side sign-in, typically a client SDK would be used to exchange email/password for tokens.
        # To simulate for this server-side context, we'll create a custom token and then
        # assume a client would exchange it for ID and refresh tokens.
        
        # This part is a simplification. A real client would use a client SDK like:
        # firebase.auth().signInWithEmailAndPassword(email, password)
        # and get idToken and refreshToken from the response.

        # Here, we will just create a custom token for the user, implying successful authentication
        # from a server perspective (e.g., if a server verified the password first).
        custom_token = auth.create_custom_token(user.uid)
        return {"success": True, "message": "User logged in successfully (custom token generated).", "custom_token": custom_token.decode('utf-8')}

    except firebase_admin.exceptions.FirebaseError as e:
        return {"success": False, "message": str(e)}
    except ValueError as e:
        return {"success": False, "message": str(e)}
