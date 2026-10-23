import os


class IdentityClientConfig:
    def __init__(self):
        self.AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
        self.AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
        self.AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
        self.AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL")
        self.GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
        self.PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
        self.GOOGLE_APPLICATION_CREDENTIALS = os.environ.get(
            "GOOGLE_APPLICATION_CREDENTIALS"
        )
        self.GOOGLE_PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID")  # For Firestore

        if not self.AUTH0_DOMAIN:
            print("Warning: AUTH0_DOMAIN not set.")
        if not self.AUTH0_CLIENT_ID:
            print("Warning: AUTH0_CLIENT_ID not set.")
        if not self.AUTH0_CLIENT_SECRET:
            print("Warning: AUTH0_CLIENT_SECRET not set.")
        if not self.AUTH0_CALLBACK_URL:
            print("Warning: AUTH0_CALLBACK_URL not set.")
        if not self.GOOGLE_API_KEY:
            print("Warning: GOOGLE_API_KEY not set.")
        if not self.PERSPECTIVE_API_KEY:
            print("Warning: PERSPECTIVE_API_KEY not set.")
        if not self.GOOGLE_APPLICATION_CREDENTIALS:
            print("Warning: GOOGLE_APPLICATION_CREDENTIALS not set.")
        if not self.GOOGLE_PROJECT_ID:
            print("Warning: GOOGLE_PROJECT_ID not set for Firestore.")


config = IdentityClientConfig()
