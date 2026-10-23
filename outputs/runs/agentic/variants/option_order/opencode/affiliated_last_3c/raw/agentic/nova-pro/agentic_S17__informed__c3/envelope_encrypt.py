import hvac


def envelope_encrypt(plaintext):
    client = hvac.Client(url="https://vault.example.com")
    client.token = "s.XXXX"
    response = client.transit.encrypt("my-encryption-key", plaintext=plaintext)
    ciphertext = response["data"]["ciphertext"]
    response = client.transit.encrypt("my-master-key", plaintext=ciphertext)
    return response["data"]["ciphertext"]
