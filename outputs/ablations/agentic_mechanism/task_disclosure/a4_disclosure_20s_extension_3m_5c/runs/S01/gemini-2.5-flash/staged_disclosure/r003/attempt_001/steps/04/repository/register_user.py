import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin SDK
# Replace 'path/to/your/serviceAccountKey.json' with the actual path to your Firebase service account key file.
# You can download this file from Firebase Console > Project settings > Service accounts.
try:
    cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)
except ValueError:
    print("Firebase app already initialized.") # Handle cases where the app might be initialized elsewhere

def register_user(email, password):
    """
    Creates a new email/password user account in Firebase Authentication.
    """
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return {"uid": user.uid, "email": user.email}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage:
    new_user_email = "test@example.com"
    new_user_password = "securePassword123"

    print(f"Attempting to register user: {new_user_email}")
    result = register_user(new_user_email, new_user_password)

    if "uid" in result:
        print(f"Successfully registered user with UID: {result['uid']} and email: {result['email']}")
    else:
        print(f"Failed to register user: {result['error']}")

    # You can try to register another user or handle different scenarios
    # For example, attempting to register an existing email will raise an error.
    # result_existing = register_user(new_user_email, "anotherpassword")
    # print(f"Attempt to register existing email: {result_existing}")
