import os

import firebase_admin
from firebase_admin import auth

from identity_models import load_identity_config


def get_config(config=None):
    return load_identity_config(config)


def get_firebase_app(config=None):
    config = get_config(config)
    try:
        return firebase_admin.get_app()
    except ValueError:
        return firebase_admin.initialize_app(options={"projectId": config["project_id"]})


def get_identity_api_key(config=None):
    config = get_config(config)
    return config.get("openai_api_key") or os.environ.get("OPENAI_API_KEY")


def verify_id_token(token, config=None):
    app = get_firebase_app(config)
    return auth.verify_id_token(token, app=app)
