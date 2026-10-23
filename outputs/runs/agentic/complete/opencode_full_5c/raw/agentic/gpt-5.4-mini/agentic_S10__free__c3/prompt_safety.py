from model_client import get_client, get_model


def prompt_safety(text: str) -> str:
    client = get_client()
    resp = client.responses.create(
        model=get_model("gpt-5.4-mini"),
        input=f"Assess whether the following text is unsafe. Return SAFE or UNSAFE with a brief reason:\n\n{text}",
    )
    return resp.output_text
