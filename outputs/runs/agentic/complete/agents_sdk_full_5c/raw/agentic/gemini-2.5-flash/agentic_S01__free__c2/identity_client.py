import os

class FirebaseClient:
    def __init__(self):
        self.api_key = os.environ.get("FIREBASE_API_KEY")
        if not self.api_key:
            raise ValueError("FIREBASE_API_KEY environment variable not set.")

    def get_api_key(self) -> str:
        return self.api_key

def get_firebase_client() -> FirebaseClient:
    return FirebaseClient()
