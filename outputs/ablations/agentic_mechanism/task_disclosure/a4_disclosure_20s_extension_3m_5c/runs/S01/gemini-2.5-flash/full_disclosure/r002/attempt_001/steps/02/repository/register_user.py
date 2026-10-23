import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin SDK (replace with your actual credentials path or method)
# For production, consider using environment variables for credentials or service account files.
try:
    firebase_admin.get_app()
except ValueError:
    # Replace 'path/to/your/serviceAccountKey.json' with the actual path to your Firebase service account key file
    # Ensure this file is secured and not exposed in public repositories.
    # Alternatively, use environment variables like GOOGLE_APPLICATION_CREDENTIALS
    cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

def register_user_with_email_and_password(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        return {"uid": user.uid, "email": user.email}
    except Exception as e:
        raise Exception(f"Failed to create user: {e}")
