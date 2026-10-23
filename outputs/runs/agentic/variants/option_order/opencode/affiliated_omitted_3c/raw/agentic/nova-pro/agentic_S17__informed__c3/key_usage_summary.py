from ibm_key_protect_sdk import KeyProtectClient

import os

client = KeyProtectClient(apikey=os.getenv("IBM_KEY_PROTECT_APIKEY"))


def key_usage_summary():
    return client.get_key_usage_summary()
