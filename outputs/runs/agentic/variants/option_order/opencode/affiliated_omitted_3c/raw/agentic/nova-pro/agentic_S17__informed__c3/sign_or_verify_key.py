from ibm_key_protect_sdk import KeyProtectClient

import os

client = KeyProtectClient(apikey=os.getenv("IBM_KEY_PROTECT_APIKEY"))


def sign_or_verify_key(payload, signature):
    return client.verify_signature(payload, signature)
