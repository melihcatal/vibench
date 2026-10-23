import os
import google.generativeai as genai

def summarize_records(records: list[dict]) -> str:
    """Summarizes a list of document records using the Google Gemini API.

    Args:
        records: A list of dictionaries, where each dictionary represents a document record.

    Returns:
        A string containing the summary of the records.
    """
    # GOOGLE_API_KEY environment variable should be set for authentication.
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro') # Using gemini-pro model family

    record_text = "\n".join([str(record) for record in records])

    prompt = f"""Please summarize the following document records:

{record_text}

Summary:"""

    response = model.generate_content(prompt)
    return response.text
