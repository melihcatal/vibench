import google.generativeai as genai
import os
from typing import Dict, Any, List

# Configure the Google Gemini API client
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))


def summarize_records(records: List[Dict[str, Any]]) -> str:
    if not records:
        return "No records to summarize."

    # Prepare the content for summarization
    text_to_summarize = "Here are some document records:\n\n"
    for i, record in enumerate(records):
        text_to_summarize += f"Document {i + 1}: {record}\n"

    # Use the Gemini Pro model for summarization
    # You might want to choose a different model based on your needs
    model = genai.GenerativeModel("gemini-pro")

    try:
        response = model.generate_content(
            f"Please summarize the following document records concisely: {text_to_summarize}"
        )
        return response.text
    except Exception as e:
        return f"Error summarizing records: {e}"
