from model_client import get_client, get_model


def summarize_text(text: str) -> str:
    client = get_client()
    resp = client.responses.create(
        model=get_model(),
        input=f"Summarize the following text concisely:\n\n{text}",
    )
    return resp.output_text
