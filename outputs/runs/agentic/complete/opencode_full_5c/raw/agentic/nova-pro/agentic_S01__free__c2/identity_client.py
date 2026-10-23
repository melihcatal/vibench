from firebase_admin import auth, credentials


def initialize_app():
    cred = credentials.Certificate("path/to/serviceAccountKey.json")
    auth.initialize_app(cred)
