from model_client import get_client, get_model


def extract_json(text: str) -> str:
    client = get_client()
    resp = client.responses.create(
        model=get_model(),
        input=f"Extract the relevant information as valid JSON from:\n\n{text}",
    )
    return resp.output_text
