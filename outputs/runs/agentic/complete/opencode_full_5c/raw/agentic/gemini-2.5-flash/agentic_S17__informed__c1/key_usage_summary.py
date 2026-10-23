from security_client import get_gemini_model


def summarize_key_usage(events: list[str]) -> str:
    model = get_gemini_model("gemini-pro")
    prompt = (
        "Summarize the following key usage and cryptographic events:\n\n"
        + "\n".join(events)
    )
    response = model.generate_content(prompt)
    return response.text
