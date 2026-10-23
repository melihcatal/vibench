import os
import google.generativeai as genai
from typing import Dict, Any


def summarize_record(document_content: Dict[str, Any]) -> str:
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")

    genai.configure(api_key=google_api_key)

    model = genai.GenerativeModel("gemini-pro")

    # Assuming the document_content has a field that can be summarized, e.g., 'text'
    # You might need to adapt this based on your actual document structure.
    text_to_summarize = document_content.get("description", "No description provided.")
    if not text_to_summarize:
        text_to_summarize = str(
            document_content
        )  # Fallback to summarizing the whole content if no specific field

    prompt = f"Summarize the following text:\n\n{text_to_summarize}"
    response = model.generate_content(prompt)
    return response.text
