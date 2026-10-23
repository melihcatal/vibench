from speech_client import get_vertex_ai_client, get_project_id, get_gcp_location
from google.cloud import aiplatform
import json


def check_script_safety(script_text: str) -> dict:
    project_id = get_project_id()
    location = get_gcp_location()
    get_vertex_ai_client(project_id, location)  # Initialize Vertex AI SDK

    # Use the GenerativeModel for content safety
    model = aiplatform.preview.generative_models.GenerativeModel(
        "gemini-pro"
    )  # Concrete model identifier

    # Craft a prompt to evaluate content safety
    prompt = f"""Evaluate the following script for potentially unsafe content, hate speech, sexual content, violence, and dangerous content. 
    Provide a JSON response with a 'safe' boolean and 'reasons' (list of strings) if not safe.

    Script: {script_text}

    JSON Response:"""

    response = model.generate_content(prompt)
    try:
        # Assuming the model returns a JSON string in the text part of the response
        safety_report_str = response.text.strip()
        safety_report = json.loads(safety_report_str)
        return safety_report
    except (json.JSONDecodeError, AttributeError):
        # Fallback if the model doesn't return clean JSON, or if response.text is not available
        return {
            "safe": False,
            "reasons": [f"Could not parse safety response from model: {response.text}"],
        }
