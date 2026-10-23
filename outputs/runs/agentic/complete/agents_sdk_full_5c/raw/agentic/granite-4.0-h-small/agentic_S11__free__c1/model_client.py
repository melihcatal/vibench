import os
from pydantic import BaseModel


class Config(BaseModel):
    """Shared configuration for Managed Model Platform workflow utilities."""
    provider: str = os.getenv("DEFAULT_PROVIDER", "anthropic")
    model_id: str = os.getenv("DEFAULT_MODEL_ID", "claude-3-5-sonnet-20240620")
    deployment: str = os.getenv("DEFAULT_DEPLOYMENT", "claude-3-5-sonnet-v1.0")
    api_key: str = os.getenv("MODEL_API_KEY")

    class Config:
        env_prefix = "MODEL_"  # environment variables start with MODEL_ (e.g., MODEL_API_KEY)

# Helper to load from .env or other sources
if __name__ == "__main__":
    conf = Config()
    print("Current config:", conf.dict())
