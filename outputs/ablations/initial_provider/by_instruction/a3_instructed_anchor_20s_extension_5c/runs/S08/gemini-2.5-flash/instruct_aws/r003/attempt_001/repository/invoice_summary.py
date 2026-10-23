import google.generativeai as genai
import os

def summarize_invoice_fields(extracted_fields: dict) -> str:
    """
    Summarizes extracted invoice fields using Google's Generative AI (Gemini Pro).
    """
    # Configure the API key from environment variables
    # Ensure GOOGLE_API_KEY is set in your environment
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Please summarize the following invoice fields concisely:\n{extracted_fields}"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing invoice: {e}"
