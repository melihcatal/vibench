import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def check_unsafe_content(script_text: str):
    """
    Checks narration scripts for unsafe content using Google Cloud Vertex AI.

    Args:
        script_text: The narration script to check.

    Returns:
        A dictionary containing safety attributes.
    """
    vertexai.init(project="your-gcp-project-id", location="us-central1") # Replace with your GCP project ID and desired location
    model = GenerativeModel("gemini-1.5-flash-001") # Using a Gemini model for safety attributes

    response = model.generate_content(
        [script_text],
        safety_settings={
            "HARM_CATEGORY_HARASSMENT": "BLOCK_ONLY_HIGH",
            "HARM_CATEGORY_HATE_SPEECH": "BLOCK_ONLY_HIGH",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_ONLY_HIGH",
            "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_ONLY_HIGH",
        },
        generation_config={
            "temperature": 0.0,
            "top_p": 0.0,
            "top_k": 1,
        }
    )

    # The safety attributes are usually in the candidate's safety_ratings
    # This might need adjustment based on the exact structure of the API response
    safety_attributes = {}
    if response.candidates:
        for candidate in response.candidates:
            if candidate.safety_ratings:
                for rating in candidate.safety_ratings:
                    safety_attributes[rating.category.name] = {
                        "score": rating.score,
                        "severity": rating.severity.name
                    }
    return safety_attributes

