import tisane


def check_safety(text):
    client = tisane.Client(api_key=os.getenv("TISANE_API_KEY"))
    response = client.moderate(text)
    return response
