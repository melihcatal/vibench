from model_client import get_client, get_model_name


def extract_json(text: str) -> str:
    client = get_client()
    response = client.models.generate_content(
        model=get_model_name("gemini-2.0-flash"),
        contents=f"Extract the relevant fields as valid JSON only:\n\n{text}",
    )
    return getattr(response, "text", "")
