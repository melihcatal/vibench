from ibm_key_protect_sdk import KeyProtectClient

import os

client = KeyProtectClient(apikey=os.getenv("IBM_KEY_PROTECT_APIKEY"))


def decrypt_payload(ciphertext):
    return client.decrypt(ciphertext)
