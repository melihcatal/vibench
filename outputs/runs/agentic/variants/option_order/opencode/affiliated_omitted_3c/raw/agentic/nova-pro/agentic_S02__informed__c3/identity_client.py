import os


def get_client():
    return requests.Session()


def get_config():
    return {
        "GOOGLE_APPLICATION_CREDENTIALS": os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    }
