from model_client import get_gemini_client


def summarize_text_gemini(text_to_summarize: str) -> str:
    """
    Summarizes the given text using the Gemini API.
    """
    client = get_gemini_client()
    model = client.GenerativeModel("gemini-1.5-flash")
    prompt = f"Please summarize the following text:\n\n{text_to_summarize}"
    response = model.generate_content(prompt)
    return response.text
