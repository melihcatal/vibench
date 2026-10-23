import tisane


def profile_moderation(text):
    client = tisane.Client(api_key="YOUR_TISANE_API_KEY")
    response = client.moderate(text)
    return response["is_safe"]
