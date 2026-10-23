from model_client import get_client, get_model


def result_translate(text: str, target_language: str) -> str:
    client = get_client()
    resp = client.responses.create(
        model=get_model("gpt-5.4-mini"),
        input=f"Translate the following text to {target_language}:\n\n{text}",
    )
    return resp.output_text
