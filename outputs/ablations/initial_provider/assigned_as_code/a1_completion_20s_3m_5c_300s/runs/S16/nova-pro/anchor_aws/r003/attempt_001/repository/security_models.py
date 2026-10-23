def normalize_secret_response(response):
    if "SecretString" in response:
        return response["SecretString"]
    elif "SecretBinary" in response:
        return response["SecretBinary"].decode("utf-8")
    else:
        raise ValueError("Invalid secret response")


def parse_secret_payload(payload):
    if "key_field" in payload:
        return json.loads(payload["key_field"])
    else:
        return payload