from model_client import client


def stream_completion(prompt: str):
    for response in client.stream_completion(prompt):
        yield response.text
