import os
import hvac


def get_client():
    return hvac.Client(url=os.getenv("VAULT_ADDR"), token=os.getenv("VAULT_TOKEN"))


def normalize_response(response):
    return response["data"]
