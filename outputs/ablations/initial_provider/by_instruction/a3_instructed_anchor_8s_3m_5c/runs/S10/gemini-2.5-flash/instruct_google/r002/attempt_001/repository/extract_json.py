import os
from google.cloud import aiplatform
from google.generativeai import GenerativeModel, configure

def extract_json(text: str) -> str:
    """
    Extracts structured JSON from the given text using a Google Generative AI model.
    """
    # Configure the Google Generative AI client
    # configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # For Vertex AI:
    # aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location=os.environ.get("GOOGLE_CLOUD_LOCATION"))
    # model = GenerativeModel(model_name="gemini-pro")

    # For Gemini API
    model = GenerativeModel(model_name="gemini-pro")

    prompt = f"Extract any structured JSON object from the following text. If no JSON is present, return an empty string. Only return the JSON object, do not include any other text:

{text}"
    response = model.generate_content(prompt)
    return response.text
