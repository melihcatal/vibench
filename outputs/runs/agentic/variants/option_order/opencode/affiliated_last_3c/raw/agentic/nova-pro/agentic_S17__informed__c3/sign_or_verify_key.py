import hvac


def sign_or_verify_key(payload):
    client = hvac.Client(url="https://vault.example.com")
    client.token = "s.XXXX"
    response = client.transit.sign("my-signing-key", payload=payload)
    return response["data"]["signature"]
