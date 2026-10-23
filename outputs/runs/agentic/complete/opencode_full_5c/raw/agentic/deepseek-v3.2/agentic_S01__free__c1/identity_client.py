import os
from typing import Optional
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class IdentityConfig:
    """Configuration for identity services."""

    def __init__(self):
        self.supabase_url = os.environ.get(
            "SUPABASE_URL", "https://your-project.supabase.co"
        )
        self.supabase_key = os.environ.get("SUPABASE_KEY", "your-anon-key")
        self.supabase_service_key = os.environ.get(
            "SUPABASE_SERVICE_KEY", "your-service-key"
        )

        # Translation service (DeepL)
        self.deepl_api_key = os.environ.get("DEEPL_API_KEY", "")
        self.deepl_api_url = "https://api.deepl.com/v2"

        # Moderation service (OpenAI)
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", "")
        self.openai_api_url = "https://api.openai.com/v1"

        # Summary service (OpenAI)
        self.openai_model = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")

        # Document store (MongoDB Atlas)
        self.mongodb_uri = os.environ.get(
            "MONGODB_URI", "mongodb+srv://user:pass@cluster.mongodb.net/"
        )
        self.mongodb_db = os.environ.get("MONGODB_DB", "identity_service")


def get_supabase_client() -> Client:
    """Get Supabase client instance."""
    config = IdentityConfig()
    return create_client(config.supabase_url, config.supabase_key)


def validate_email(email: str) -> bool:
    """Validate email format."""
    import re

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_password(password: str) -> tuple[bool, str]:
    """Validate password strength."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"
    return True, "Password is valid"


def normalize_user_data(user_data: dict) -> dict:
    """Normalize user data for storage."""
    normalized = {
        "email": user_data.get("email", "").lower().strip(),
        "display_name": user_data.get("display_name", "").strip(),
        "created_at": user_data.get("created_at"),
        "updated_at": user_data.get("updated_at"),
        "metadata": user_data.get("metadata", {}),
    }

    # Remove None values
    return {k: v for k, v in normalized.items() if v is not None}
