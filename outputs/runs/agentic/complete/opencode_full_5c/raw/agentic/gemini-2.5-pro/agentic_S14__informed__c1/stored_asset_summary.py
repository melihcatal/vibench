import os
import google.generativeai as genai
from storage_models import SummaryResult


def summarize_content(content: str) -> SummaryResult:
    """
    Summarizes content using the Google Gemini API.
    Requires GOOGLE_API_KEY to be set in the environment.

    :param content: The text content to summarize.
    :return: A SummaryResult object.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")

    prompt = f"Please summarize the following content:\n\n{content}"
    response = model.generate_content(prompt)

    return SummaryResult(summary_text=response.text)
