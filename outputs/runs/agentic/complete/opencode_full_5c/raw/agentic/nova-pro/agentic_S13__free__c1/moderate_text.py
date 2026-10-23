import safety_client


def score_text(text):
    client = safety_client.get_client()
    response = client.moderate_text(text)
    return response.get("safety_score")
