from model_client import client


def stream_platform_generation(prompt: str):
    for response in client.generate_text_stream(prompt=prompt):
        yield response
