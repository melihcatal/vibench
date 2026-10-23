from ibm_key_protect_sdk import KeyProtectClient

import os

client = KeyProtectClient(apikey=os.getenv("IBM_KEY_PROTECT_APIKEY"))


def envelope_encrypt(payload):
    key = client.generate_key()
    encrypted_payload = client.encrypt(payload, key)
    return encrypted_payload, key
