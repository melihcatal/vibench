import os


def get_client():
    return KeyProtectClient(apikey=os.getenv("IBM_KEY_PROTECT_APIKEY"))
