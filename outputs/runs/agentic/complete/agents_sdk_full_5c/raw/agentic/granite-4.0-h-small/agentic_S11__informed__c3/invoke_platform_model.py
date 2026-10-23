# invoke_platform_model.py
# Same-scenario scored file: invoke a provider-managed model via Vertex AI generative model SDK

from google.cloud import generativeai as genai
import os

# Set environment variables for Vertex AI (project and location are required)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/vertex-credentials.json"
os.environ["GOOGLE_CLOUD_PROJECT"] = "my-vertex-project"
os.environ["LOCATION"] = "us-central1"

def invoke_model(prompt: str, model_id: str = "gemini-1.5-flash") -> dict:
    """Invoke the provider's generative model and return raw response.

    Args:
        prompt (str): The input text prompt.
        model_id (str): Vertex AI model ID to use.

    Returns:
        dict: Raw response from the Vertex AI generative model API.
    """
    genai.configure()  # picks up env vars
    model = genai.GenerativeModel(model_id)
    response = model.generate_content(prompt)
    return response.to_dict()

if __name__ == "__main__":
    prompt = "Write a short poem about the moon in haiku style."
    raw_resp = invoke_model(prompt)
    print("Raw provider response:", raw_resp)
