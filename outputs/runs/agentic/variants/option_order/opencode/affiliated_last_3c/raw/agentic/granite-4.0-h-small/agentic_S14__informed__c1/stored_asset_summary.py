import os
from google.cloud import generativeai as genai
from storage_client import ManagedStorageClient


def summarize_asset(bucket_name: str, object_key: str) -> str:
    """Generate a concise summary of content extracted from a stored asset using Gemini.

    Assumes the object contains textual content (PDF, DOCX, etc.) that has already been extracted.
    """
    # Load extracted text from storage (placeholder: here we call OCR to illustrate end-to-end)
    # In a real workflow, replace this with a call to the OCR step or retrieve the text from prior processing.
    extracted_text = "Sample text to be summarized."
    # Configure Gemini generative model (vertex AI endpoint determined by env vars)
    genai.configure(
        api_key=os.getenv("GEMINI_API_KEY"), project=os.getenv("GEMINI_PROJECT_ID")
    )
    model = genai.GenerativeModel(
        "gemini-1.5-flash"
    )  # example model ID; actual ID may differ
    prompt = f"Summarize the following document in 2-3 sentences:\n\n{extracted_text}"
    response = model.generate_content(prompt)
    return response.text.strip()
