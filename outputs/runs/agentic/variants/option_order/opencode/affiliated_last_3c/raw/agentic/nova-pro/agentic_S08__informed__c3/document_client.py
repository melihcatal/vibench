import os


def get_client():
    return {
        "access_key_id": os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        "access_key_secret": os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    }
