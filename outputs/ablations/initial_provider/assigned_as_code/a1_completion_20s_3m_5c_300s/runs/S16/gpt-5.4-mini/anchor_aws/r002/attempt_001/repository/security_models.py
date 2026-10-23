import json


def secret_text(response):
    if "SecretString" in response:
        return response["SecretString"]
    if "SecretBinary" in response:
        return response["SecretBinary"].decode("utf-8")
    return ""


def parse_json_secret_value(value):
    if isinstance(value, str):
        return json.loads(value)
    return value


def normalize_label_text(value):
    return " ".join(str(value).split())
