import firebase_admin
from firebase_admin import credentials, auth
import os

# Initialize Firebase Admin SDK
# Make sure to set the GOOGLE_APPLICATION_CREDENTIALS environment variable
# pointing to your service account key file.
# For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/serviceAccountKey.json"
if not firebase_admin._apps:
    try:
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        print("Please ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set and points to a valid service account key file.")
        exit(1)

def sign_in_with_email_and_password(email, password):
    """
    Signs in a user with email and password using Firebase Authentication
    and returns the ID token.
    Note: The Firebase Admin SDK does not directly provide the client-side
    sign-in functionality that returns refresh tokens directly. This
    function demonstrates how to verify credentials on the backend.
    For client-side sign-in, you would typically use a client-side SDK
    (e.g., Firebase JS SDK, Android SDK, iOS SDK) to get ID and refresh tokens.
    To verify these tokens on the backend, you can use verify_id_token.
    """
    try:
        # For server-side, you typically verify ID tokens obtained from client-side login.
        # The Admin SDK does not perform email/password sign-in directly for users to obtain tokens.
        # Instead, it manages users and verifies client-issued tokens.
        # This function simulates a successful authentication by attempting to get a user by email.
        # In a real scenario, the client would send the email and password to a custom endpoint,
        # which would then use the client-side Firebase SDK to sign in and get tokens,
        # or use a custom authentication system.

        # To demonstrate interaction with Firebase Auth for a user, we will attempt to get the user by email.
        # In a true client-server flow, the client would sign in and send its ID token to the server.
        user = auth.get_user_by_email(email)
        print(f"User {user.uid} found by email.")

        # In a real client-server flow, you would receive an ID token from the client
        # after a successful email/password sign-in on the client side.
        # For demonstration purposes, we acknowledge user existence here.
        # If you were to create custom tokens for a custom authentication system:
        # custom_token = auth.create_custom_token(user.uid)
        # return custom_token

        # This part is conceptual for returning "tokens" in a server-side context
        # without a direct client-side sign-in flow through the Admin SDK.
        # In practice, you might generate a custom token to send back to the client
        # or verify an ID token sent from the client.
        return {"message": "User authenticated successfully (server-side conceptual). Client-side sign-in required for direct ID/Refresh tokens.", "uid": user.uid}

    except auth.UserNotFoundError:
        return {"error": "No user found with that email address."}
    except Exception as e:
        return {"error": f"Error during sign-in: {e}"}

if __name__ == "__main__":
    # Example usage (replace with actual email and password for testing)
    test_email = os.environ.get("FIREBASE_TEST_EMAIL")
    test_password = os.environ.get("FIREBASE_TEST_PASSWORD")

    if test_email and test_password:
        print(f"Attempting to sign in with email: {test_email}")
        result = sign_in_with_email_and_password(test_email, test_password)
        print(result)
    else:
        print("Please set FIREBASE_TEST_EMAIL and FIREBASE_TEST_PASSWORD environment variables for testing.")
        print("Also ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set and points to your service account key file.")

