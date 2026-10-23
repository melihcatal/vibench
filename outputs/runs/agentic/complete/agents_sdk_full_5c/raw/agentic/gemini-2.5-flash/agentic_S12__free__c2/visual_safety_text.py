import vertexai
from vertexai.preview.generative_models import GenerativeModel
from vision_client import initialize_vertexai
from typing import Dict, Any

def check_text_safety(text_content: str, project_id: str, location: str) -> Dict[str, Any]:
    """Checks generated visual labels or descriptions for unsafe text using Gemini Pro."""
    initialize_vertexai(project_id, location) # e.g., "your-gcp-project-id", "us-central1"
    model = GenerativeModel("gemini-pro")

    # Use a prompt to instruct the model to perform a safety check
    prompt = f"""Analyze the following text for safety concerns such as toxicity, harassment, hate speech, dangerous content, or sexual content.
Provide a clear assessment for each category (SAFE/UNSAFE/BORDERLINE) and explain why if it's not SAFE.

Text: "{text_content}"
"""
    response = model.generate_content([prompt])
    # The response will contain the model's text assessment.
    # For a more structured output, you might parse the text or guide the model to output JSON.
    # For this example, we return the raw text response as a dict value.
    return {"safety_assessment_text": response.text}

if __name__ == '__main__':
    # Replace with your actual GCP project ID and region
    project_id = "your-gcp-project-id"
    location = "us-central1"

    test_text_safe = "A beautiful sunny day at the park."
    test_text_unsafe = "I hate you and your stupid ideas."

    print("Checking safe text:")
    result_safe = check_text_safety(test_text_safe, project_id, location)
    print(result_safe)

    print("\nChecking unsafe text:")
    result_unsafe = check_text_safety(test_text_unsafe, project_id, location)
    print(result_unsafe)
