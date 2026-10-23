import os
import google.generativeai as genai


def summarize_stored_asset(asset_content: str) -> str:
    """
    Summarizes text content using the Google Gemini API.

    Requires the GOOGLE_API_KEY environment variable to be set.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")

    prompt = f"Please summarize the following content:\n\n{asset_content}"

    response = model.generate_content(prompt)

    return response.text
