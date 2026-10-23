import google.generativeai as genai
import os

def summarize_invoice_fields(invoice_fields: dict) -> str:
    """
    Summarizes extracted invoice fields using Google's Gemini API.

    Args:
        invoice_fields: A dictionary containing the extracted invoice fields.

    Returns:
        A string containing the summary of the invoice fields.
    """
    # Configure the Google Generative AI API with an API key from environment variables
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

    # Initialize the Generative Model (using a specific model ID)
    model = genai.GenerativeModel('gemini-pro')

    # Construct the prompt for summarization
    prompt = f"""
    Please summarize the following invoice fields in a concise manner:

    {invoice_fields}

    Focus on key information such as vendor, total amount, date, and a brief overview of line items if available.
    """

    # Generate content using the model
    response = model.generate_content(prompt)

    return response.text
