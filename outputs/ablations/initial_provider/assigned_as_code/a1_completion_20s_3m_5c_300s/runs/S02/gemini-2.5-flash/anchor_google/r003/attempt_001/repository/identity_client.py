import os
from typing import Dict, Any


def get_auth0_config() -> Dict[str, Any]:
    return {
        "AUTH0_DOMAIN": os.getenv("AUTH0_DOMAIN"),
        "AUTH0_CLIENT_ID": os.getenv("AUTH0_CLIENT_ID"),
        "AUTH0_CLIENT_SECRET": os.getenv("AUTH0_CLIENT_SECRET"),
        "AUTH0_API_AUDIENCE": os.getenv("AUTH0_API_AUDIENCE", f"https://{{os.getenv('AUTH0_DOMAIN')}}/api/v2/"),
    }
