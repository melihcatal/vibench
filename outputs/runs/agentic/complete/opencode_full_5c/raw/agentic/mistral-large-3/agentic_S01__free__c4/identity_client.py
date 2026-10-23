import os
from typing import Optional
from firebase_admin import auth


class IdentityClient:
    @staticmethod
    def get_firebase_user(user_id: str) -> Optional[auth.UserRecord]:
        try:
            return auth.get_user(user_id)
        except Exception:
            return None

    @staticmethod
    def validate_token(id_token: str) -> Optional[dict]:
        try:
            return auth.verify_id_token(id_token)
        except Exception:
            return None

    @staticmethod
    def get_project_id() -> str:
        return os.getenv("FIREBASE_PROJECT_ID")
