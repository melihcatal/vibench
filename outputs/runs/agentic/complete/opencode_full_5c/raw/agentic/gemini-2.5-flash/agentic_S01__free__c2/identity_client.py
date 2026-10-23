import os


class FirebaseConfig:
    """
    Configuration for Firebase Authentication.
    Assumes FIREBASE_API_KEY is set in environment variables for client-side API calls.
    For server-side operations (like creating users), Firebase Admin SDK setup is assumed
    to be handled by environment-specific configuration (e.g., GOOGLE_APPLICATION_CREDENTIALS).
    """

    API_KEY = os.environ.get("FIREBASE_API_KEY")


class GoogleCloudConfig:
    """
    Configuration for Google Cloud services.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    pointing to a service account key file for authentication.
    """

    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    API_KEY = os.environ.get("GOOGLE_API_KEY")
