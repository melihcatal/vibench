from model_client import client


def summarize_text(text: str) -> str:
    response = client.summarize(text)
    return response.text
