import os
from google.cloud import aiplatform
from google.generativeai import GenerativeModel, configure

def summarize_text(text: str) -> str:
    """
    Summarizes the given text using a Google Generative AI model.
    """
    # Configure the Google Generative AI client
    # Replace with your project ID and location if using Vertex AI directly
    # Or set GOOGLE_API_KEY environment variable for Gemini API
    # configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # For Vertex AI:
    # aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location=os.environ.get("GOOGLE_CLOUD_LOCATION"))
    # model = GenerativeModel(model_name="gemini-pro")

    # For Gemini API (example with direct API key, prefer environment variable)
    model = GenerativeModel(model_name="gemini-pro")


    prompt = f"Summarize the following text:

{text}"
    response = model.generate_content(prompt)
    return response.text

