from model_client import get_client, get_model_name


def summarize_text(text: str) -> str:
    client = get_client()
    response = client.models.generate_content(
        model=get_model_name("gemini-2.0-flash"),
        contents=f"Summarize the following text in a concise paragraph:\n\n{text}",
    )
    return getattr(response, "text", "")
