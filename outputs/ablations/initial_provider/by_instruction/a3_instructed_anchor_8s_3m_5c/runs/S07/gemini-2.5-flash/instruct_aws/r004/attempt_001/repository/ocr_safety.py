import os
from vertexai.preview.generative_models import GenerativeModel, Part # Google Cloud SDK for Vertex AI
import vertexai

def check_safety(text: str) -> dict:
    """
    Checks extracted document text for unsafe content using Google Cloud Vertex AI.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set
    and gcloud auth configured for Vertex AI access.
    """
    # Initialize Vertex AI with a project and location
    # The Vertex AI API endpoint is implicitly used by the client
    vertexai.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location=os.environ.get("GOOGLE_CLOUD_REGION", "us-central1"))

    # Using a specific model for safety assessment, e.g., gemini-pro
    # This is a provider-specific model ID
    model = GenerativeModel("gemini-pro") 

    prompt = f"Analyze the following text for safety and provide a safety score or categories if it contains harmful content (e.g., hate speech, self-harm, sexual, violence). Return a JSON object with a 'safety_score' (0-1, 1 being most harmful) and 'safety_categories' (list of strings). If no harmful content, score should be 0 and categories empty. Text: \"\"\"{text}\"\"\""
    
    response = model.generate_content(prompt)
    
    # The response object from Vertex AI will contain safety attributes
    # For this example, we're asking the model to self-assess and return JSON
    # In a real scenario, you'd parse model.candidates[0].safety_attributes
    # For simplicity, we are assuming the model returns the requested JSON directly.
    # More robust parsing and error handling would be needed for production.
    try:
        return response.text # Assuming the model directly returns the JSON string
    except AttributeError:
        return {"error": "Could not get safety assessment from model.", "full_response": str(response)}

