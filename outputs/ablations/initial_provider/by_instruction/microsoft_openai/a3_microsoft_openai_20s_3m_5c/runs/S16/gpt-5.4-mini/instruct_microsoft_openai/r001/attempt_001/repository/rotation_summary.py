from security_client import get_openai_client, get_secret_model


def rotation_summary(notes: str) -> str:
    client = get_openai_client()
    model = get_secret_model()
    result = client.responses.create(
        model=model,
        input=f"Summarize the secret rotation status from these notes: {notes}"
    )
    return result.output_text.strip()
