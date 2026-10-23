from model_client import get_client, get_model


def spoken_brief(text: str) -> str:
    client = get_client()
    resp = client.responses.create(
        model=get_model("gpt-5.4-mini"),
        input=f"Rewrite the following as a short spoken brief:\n\n{text}",
    )
    return resp.output_text
