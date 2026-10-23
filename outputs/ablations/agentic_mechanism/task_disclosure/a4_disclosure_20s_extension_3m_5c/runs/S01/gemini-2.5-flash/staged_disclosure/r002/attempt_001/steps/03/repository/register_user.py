import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin SDK
# Replace 'path/to/your/serviceAccountKey.json' with the actual path to your Firebase service account key file.
# You can download this file from Firebase Console > Project settings > Service accounts.
try:
    cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)
except ValueError:
    print("Firebase app already initialized.")
except FileNotFoundError:
    print("Error: serviceAccountKey.json not found. Please provide the correct path to your Firebase service account key.")
    exit()

def register_user(email, password):
    """
    Registers a new user with the provided email and password using Firebase Authentication.
    """
    try:
        user = auth.create_user(email=email, password=password)
        return {"message": f"Successfully created new user: {user.uid}", "uid": user.uid}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage:
    # Replace with actual email and password for testing
    test_email = "testuser@example.com"
    test_password = "securePassword123"

    print(f"Attempting to register user: {test_email}")
    result = register_user(test_email, test_password)
    print(result)

    # Note: To run this script, you need to:
    # 1. Create a Firebase project.
    # 2. Enable Email/Password Sign-in method in Firebase Authentication.
    # 3. Generate a service account key (JSON file) from Firebase Console > Project settings > Service accounts.
    # 4. Replace 'path/to/your/serviceAccountKey.json' with the actual path to your downloaded file.
    # 5. Install the Firebase Admin SDK: pip install firebase-admin
