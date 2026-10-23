import os
import google.generativeai as genai


def record_summary(document_text: str) -> str:
    """
    Summarizes a document's text content using the Google Gemini API.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")

    prompt = f"Summarize the following document content:\n\n{document_text}"

    response = model.generate_content(prompt)

    return response.text
