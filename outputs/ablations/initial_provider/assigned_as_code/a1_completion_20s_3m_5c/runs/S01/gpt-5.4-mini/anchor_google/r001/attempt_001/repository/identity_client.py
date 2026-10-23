import os


def get_identity_config(config=None):
    config = config or {}
    return {
        "project_id": config.get("project_id") or os.environ["FIREBASE_PROJECT_ID"],
        "api_key": config.get("api_key") or os.environ.get("FIREBASE_WEB_API_KEY"),
    }
