import os
from typing import Dict, Any, Optional


def get_mongodb_atlas_uri() -> str:
    uri = os.getenv("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable is required.")
    return uri
