import os
import firebase_admin
from firebase_admin import auth, credentials
from typing import Optional, Dict, Any


class IdentityClient:
    """Client helper utilities for Firebase Authentication."""

    def __init__(self):
        self._initialized = False
        self._api_key = os.getenv("FIREBASE_API_KEY")
        self._cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    def initialize_admin_sdk(self) -> None:
        """Initialize Firebase Admin SDK if not already initialized."""
        if not firebase_admin._apps:
            if not self._cred_path:
                raise ValueError(
                    "GOOGLE_APPLICATION_CREDENTIALS environment variable not set"
                )
            cred = credentials.Certificate(self._cred_path)
            firebase_admin.initialize_app(cred)
        self._initialized = True

    def get_api_key(self) -> str:
        """Get Firebase API key for REST API calls."""
        if not self._api_key:
            raise ValueError("FIREBASE_API_KEY environment variable not set")
        return self._api_key

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user information by email using Admin SDK."""
        self.initialize_admin_sdk()
        try:
            user_record = auth.get_user_by_email(email)
            return self._normalize_user_record(user_record)
        except auth.UserNotFoundError:
            return None
        except Exception as e:
            raise RuntimeError(f"Failed to get user: {str(e)}")

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user information by user ID using Admin SDK."""
        self.initialize_admin_sdk()
        try:
            user_record = auth.get_user(user_id)
            return self._normalize_user_record(user_record)
        except auth.UserNotFoundError:
            return None
        except Exception as e:
            raise RuntimeError(f"Failed to get user: {str(e)}")

    def update_user_profile(
        self, user_id: str, display_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update user profile information."""
        self.initialize_admin_sdk()
        try:
            update_params = {}
            if display_name is not None:
                update_params["display_name"] = display_name

            user_record = auth.update_user(user_id, **update_params)
            return self._normalize_user_record(user_record)
        except auth.UserNotFoundError:
            raise ValueError("User not found")
        except Exception as e:
            raise RuntimeError(f"Failed to update user: {str(e)}")

    def _normalize_user_record(self, user_record) -> Dict[str, Any]:
        """Normalize Firebase user record to consistent format."""
        return {
            "user_id": user_record.uid,
            "email": user_record.email,
            "display_name": user_record.display_name,
            "email_verified": user_record.email_verified,
            "disabled": user_record.disabled,
            "created_at": user_record.user_metadata.creation_timestamp,
            "last_login_at": user_record.user_metadata.last_sign_in_timestamp,
            "provider_data": [
                {
                    "provider_id": provider.provider_id,
                    "uid": provider.uid,
                    "email": provider.email,
                    "display_name": provider.display_name,
                }
                for provider in user_record.provider_data
            ],
        }

    def verify_id_token(self, id_token: str) -> Dict[str, Any]:
        """Verify Firebase ID token and return decoded claims."""
        self.initialize_admin_sdk()
        try:
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except auth.ExpiredIdTokenError:
            raise ValueError("Token has expired")
        except auth.InvalidIdTokenError:
            raise ValueError("Invalid token")
        except Exception as e:
            raise RuntimeError(f"Token verification failed: {str(e)}")
