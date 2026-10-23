import os
from typing import Dict, Any, Optional
from firebase_admin import auth, initialize_app
from firebase_admin.exceptions import FirebaseError


class IdentityClient:
    """
    Client helper for Firebase Authentication operations.
    """

    def __init__(self):
        if not auth._apps:
            initialize_app(options={"projectId": os.getenv("FIREBASE_PROJECT_ID")})

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Fetches user details from Firebase Authentication."""
        try:
            user = auth.get_user(user_id)
            return {
                "uid": user.uid,
                "email": user.email,
                "email_verified": user.email_verified,
                "display_name": user.display_name,
            }
        except FirebaseError:
            return None
