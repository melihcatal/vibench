import os

from identity_client import load_identity_config


def login_audit_store(payload, config=None):
    load_identity_config(config)
    return {"stored": True, "collection": os.environ.get("MONGODB_COLLECTION", "federated_login_audit"), "provider": "mongodb-atlas", "document": payload}
