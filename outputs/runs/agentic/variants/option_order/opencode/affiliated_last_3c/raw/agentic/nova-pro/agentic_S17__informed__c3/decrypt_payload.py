import hvac


def decrypt_payload(ciphertext):
    client = hvac.Client(url="https://vault.example.com")
    client.token = "s.XXXX"
    response = client.transit.decrypt("my-encryption-key", ciphertext=ciphertext)
    return response["data"]["plaintext"]
