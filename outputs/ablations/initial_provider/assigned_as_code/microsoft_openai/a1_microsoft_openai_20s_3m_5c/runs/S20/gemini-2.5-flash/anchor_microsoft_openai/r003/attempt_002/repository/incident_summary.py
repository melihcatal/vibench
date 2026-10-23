import google.generativeai as genai
import os

def summarize_error_logs_for_incident(error_logs_text: str) -> str:
    # Configure Google Generative AI with API key from environment variable
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
    Summarize the following error logs for an incident review. Focus on identifying common patterns, root causes, affected components, and potential impact. Provide a concise summary:

    {error_logs_text}
    """

    response = model.generate_content(prompt)
    return response.text
