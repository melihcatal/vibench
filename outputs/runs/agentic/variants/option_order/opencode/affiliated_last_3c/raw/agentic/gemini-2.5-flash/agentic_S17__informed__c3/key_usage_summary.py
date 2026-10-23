import google.generativeai as genai
import os


def summarize_key_usage(log_data: str) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""Summarize the following key usage and cryptographic event logs. Highlight any unusual activity or potential security concerns.  Make the summary concise and easy to understand for a security reviewer.

Logs:
{log_data}

Summary:"""

    response = model.generate_content(prompt)
    return response.text
