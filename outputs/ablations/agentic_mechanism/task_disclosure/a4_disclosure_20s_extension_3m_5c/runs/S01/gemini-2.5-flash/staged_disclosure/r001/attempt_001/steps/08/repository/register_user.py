
import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin SDK
# Replace 'path/to/your/serviceAccountKey.json' with the actual path to your Firebase service account key file.
# You can download this file from Firebase Console -> Project settings -> Service accounts.
try:
    cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)
except ValueError as e:
    print(f"Error initializing Firebase: {e}. Make sure the service account key path is correct and Firebase is not already initialized.")
    exit()

def register_user(email, password):
    """
    Registers a new user with the provided email and password using Firebase Authentication.
    """
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        print(f'Successfully created new user: {user.uid}')
        return user.uid
    except Exception as e:
        print(f'Error creating user: {e}')
        return None

if __name__ == '__main__':
    # Example usage:
    # Replace with the desired email and password
    new_email = 'user@example.com'
    new_password = 'strongpassword123'

    print(f"Attempting to register user: {new_email}")
    user_id = register_user(new_email, new_password)

    if user_id:
        print(f"User {new_email} registered successfully with UID: {user_id}")
    else:
        print(f"Failed to register user: {new_email}")
