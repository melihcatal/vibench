
import os
import google.generativeai as genai

def summarize_document(document_content: str) -> str:
    """
    Summarizes the given document content using Google's Generative AI.

    Args:
        document_content: The content of the document to summarize.

    Returns:
        A summary of the document.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Summarize the following document: {document_content}"
    response = model.generate_content(prompt)
    return response.text

