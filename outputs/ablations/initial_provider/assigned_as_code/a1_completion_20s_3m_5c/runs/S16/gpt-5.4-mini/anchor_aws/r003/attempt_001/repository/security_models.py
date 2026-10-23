import json


def extract_json_secret(secret_text, key=None):
    data = json.loads(secret_text)
    return data[key] if key else data


def select_secret_value(response):
    if "SecretString" in response:
        return response["SecretString"]
    return response["SecretBinary"].decode("utf-8")
