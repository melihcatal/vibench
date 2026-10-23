import os

# Configuration for Firebase Web API Key
# This key is used for client-side operations (login, refresh, password reset)
# It can be found in your Firebase project settings -> Project settings -> General -> Web API Key
FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")

# Path to Firebase Admin SDK service account key JSON file
# This key is used for server-side administration (user creation)
# Download from Firebase project settings -> Service accounts -> Generate new private key
FIREBASE_SERVICE_ACCOUNT_KEY_PATH = os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY_PATH", "./serviceAccountKey.json")

# Define common endpoints or prefixes if needed
FIREBASE_IDENTITY_TOOLKIT_URL = "https://identitytoolkit.googleapis.com/v1/accounts"
FIREBASE_SECURETOKEN_URL = "https://securetoken.googleapis.com/v1/token"
