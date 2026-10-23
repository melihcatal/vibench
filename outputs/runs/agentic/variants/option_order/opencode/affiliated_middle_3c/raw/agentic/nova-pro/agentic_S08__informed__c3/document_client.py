import os


def get_client():
    return os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"), os.getenv(
        "ALIBABA_CLOUD_ACCESS_KEY_SECRET"
    )
