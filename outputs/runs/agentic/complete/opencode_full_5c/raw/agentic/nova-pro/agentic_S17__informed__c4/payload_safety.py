import tisane


def payload_safety(text):
    client = tisane.Client(api_key="your_tisane_api_key")
    response = client.moderate(text)
    return response["is_safe"]
