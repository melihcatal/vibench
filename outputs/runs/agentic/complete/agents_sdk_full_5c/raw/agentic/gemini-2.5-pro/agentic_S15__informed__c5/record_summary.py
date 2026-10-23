import os
import google.generativeai as genai

def summarize_record(record_text: str) -> str:
    """
    Summarizes the provided text using the Google Gemini API.

    :param record_text: The text content of the record to summarize.
    :return: The generated summary as a string.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Please provide a concise summary of the following document:\n\n---\n{record_text}\n---"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        raise
