import os


def get_perspective_api_key():
    return os.getenv("PERSPECTIVE_API_KEY")


def get_tisane_api_key():
    return os.getenv("TISANE_API_KEY")


def get_alibaba_cloud_access_keys():
    return os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"), os.getenv(
        "ALIBABA_CLOUD_ACCESS_KEY_SECRET"
    )


def get_azure_content_safety_keys():
    return os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"), os.getenv(
        "AZURE_CONTENT_SAFETY_KEY"
    )
