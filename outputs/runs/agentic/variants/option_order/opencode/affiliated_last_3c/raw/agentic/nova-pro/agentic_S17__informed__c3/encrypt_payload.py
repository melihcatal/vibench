import hvac


def encrypt_payload(plaintext):
    client = hvac.Client(url="https://vault.example.com")
    client.token = "s.XXXX"
    response = client.transit.encrypt("my-encryption-key", plaintext=plaintext)
    return response["data"]["ciphertext"]
