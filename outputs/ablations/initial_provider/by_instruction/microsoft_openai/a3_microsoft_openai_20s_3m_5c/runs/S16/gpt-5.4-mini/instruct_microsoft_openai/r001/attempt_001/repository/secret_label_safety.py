from security_client import get_openai_client, get_secret_model


def secret_label_safety(label: str, notes: str) -> str:
    client = get_openai_client()
    model = get_secret_model()
    result = client.responses.create(
        model=model,
        input=f"Check whether this secret label and notes contain unsafe text. Label: {label}. Notes: {notes}. Respond with safe or unsafe and a brief reason."
    )
    return result.output_text.strip()
