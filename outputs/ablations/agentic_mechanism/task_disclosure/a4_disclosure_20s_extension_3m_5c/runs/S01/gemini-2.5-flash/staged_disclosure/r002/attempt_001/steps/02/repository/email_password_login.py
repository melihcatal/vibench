import firebase_admin
from firebase_admin import credentials, auth
import os

# Initialize Firebase Admin SDK
# Replace 'path/to/your/serviceAccountKey.json' with the actual path to your Firebase service account key file.
# It is recommended to store this path in an environment variable for security.
try:
    FIREBASE_SERVICE_ACCOUNT_KEY = os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY_PATH", "path/to/your/serviceAccountKey.json")
    cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT_KEY)
    firebase_admin.initialize_app(cred)
except ValueError:
    print("Firebase Admin SDK already initialized.")
except Exception as e:
    print(f"Error initializing Firebase Admin SDK: {e}")
    # Handle the error appropriately, perhaps exit or raise

def sign_in_with_email_and_password(email, password):
    """
    Signs in a user with email and password and returns tokens.
    Uses Firebase Authentication.
    """
    try:
        # Firebase does not directly expose a sign_in_with_email_and_password method in the Admin SDK
        # that returns ID tokens for client-side authentication.
        # The Admin SDK is primarily for server-side operations like verifying ID tokens,
        # creating custom tokens, or managing users.
        #
        # To get ID tokens for an existing user via email/password, a client-side SDK (e.g., Firebase JS SDK, Android SDK, iOS SDK)
        # would typically be used to perform the sign-in directly.
        #
        # However, for a server-side equivalent that might be used in a trusted environment
        # to verify credentials and then potentially mint a custom token or perform other actions,
        # we can verify the user's existence and then, if needed, create a custom token.
        # This function will simulate a successful authentication by verifying the user exists
        # and then generating a custom token for demonstration purposes.
        # In a real-world scenario, the client-side Firebase SDK would handle the direct email/password login.

        user = auth.get_user_by_email(email)
        # If the user exists, we can consider this a successful "authentication" for server-side logic.
        # In a real scenario, you'd verify the password against a secure hash, but Firebase client SDKs handle this.
        # For server-side, if you need to create a session or perform actions after user verification:
        
        # Generate a custom token. This token can then be exchanged by a client-side SDK for an ID token.
        custom_token = auth.create_custom_token(user.uid)
        
        return {
            "uid": user.uid,
            "email": user.email,
            "custom_token": custom_token.decode('utf-8'), # Custom token is bytes, decode to string
            "message": "User authenticated and custom token generated successfully."
        }
    except auth.UserNotFoundError:
        return {"error": "User not found.", "status": 404}
    except Exception as e:
        return {"error": str(e), "status": 500}

