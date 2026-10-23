from security_client import get_openai_client, get_secret_model


def runbook_translate(notes: str, target_language: str) -> str:
    client = get_openai_client()
    model = get_secret_model()
    result = client.responses.create(
        model=model,
        input=f"Translate these secret-rotation runbook notes into {target_language}: {notes}"
    )
    return result.output_text.strip()
