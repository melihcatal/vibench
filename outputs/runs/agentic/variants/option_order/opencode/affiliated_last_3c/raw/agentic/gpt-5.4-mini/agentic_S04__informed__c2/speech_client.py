import os


def get_provider_name():
    return "assemblyai"


def get_api_key():
    return os.getenv("ASSEMBLYAI_API_KEY", "")


def get_headers():
    return {"authorization": get_api_key(), "content-type": "application/json"}


def get_upload_headers():
    return {"authorization": get_api_key()}


def get_base_url():
    return "https://api.assemblyai.com/v2"
