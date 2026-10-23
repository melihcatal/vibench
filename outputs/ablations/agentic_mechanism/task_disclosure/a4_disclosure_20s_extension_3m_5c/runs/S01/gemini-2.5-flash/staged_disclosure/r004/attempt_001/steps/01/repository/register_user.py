import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin SDK
# Replace 'path/to/your/serviceAccountKey.json' with the actual path to your Firebase service account key file.
# You can download this file from Firebase Console -> Project settings -> Service accounts.
# For production environments, consider using environment variables to store the path or the credentials directly.
try:
    cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)
except ValueError as e:
    print(f"Error initializing Firebase Admin SDK: {e}")
    print("Please ensure 'path/to/your/serviceAccountKey.json' is correct and accessible.")
    exit(1)

def register_user(email, password):
    """
    Registers a new user with the provided email and password using Firebase Authentication.
    """
    try:
        user = auth.create_user(email=email, password=password)
        print(f'Successfully created new user: {user.uid}')
        return user.uid
    except Exception as e:
        print(f'Error creating user: {e}')
        return None

if __name__ == '__main__':
    # Example usage:
    # In a real application, you would get email and password from user input
    # For demonstration, we use placeholder values.
    test_email = 'test@example.com'
    test_password = 'securePassword123' # Firebase requires password to be at least 6 characters

    print(f"Attempting to register user: {test_email}")
    user_id = register_user(test_email, test_password)
    if user_id:
        print(f"User {test_email} registered successfully with UID: {user_id}")
    else:
        print(f"Failed to register user: {test_email}")
