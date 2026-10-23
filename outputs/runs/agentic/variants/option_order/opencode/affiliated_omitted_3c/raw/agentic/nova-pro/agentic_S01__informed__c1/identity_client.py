import os


def get_client():
    return IDaaSClient(
        access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )


def normalize_response(response):
    return {"user_id": response.user_id, "status": response.status}
