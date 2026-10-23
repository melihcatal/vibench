import os
import vertexai
from vertexai.language_models import TextGenerationModel

def check_log_safety(log_message: str) -> dict:
    """
    Checks the given log message for unsafe content using Google Cloud's Vertex AI.

    Args:
        log_message: The text of the log message to check.

    Returns:
        A dictionary containing the safety assessment.
    """
    # Initialize Vertex AI with your Google Cloud project and location
    # Replace 'your-project-id' and 'your-location' with your actual project ID and desired location.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or gcloud is configured.
    vertexai.init(project=os.getenv('GOOGLE_CLOUD_PROJECT'), location=os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1'))

    model = TextGenerationModel.from_pretrained("gemini-pro")

    prompt = f"""
    Analyze the following log message for any unsafe content, including but not limited to:
    - Hate speech
    - Self-harm
    - Sexual content
    - Violence
    - Harassment

    Log Message: "{log_message}"

    Provide a safety assessment. If unsafe content is detected, describe the nature of the unsafety.
    Return the assessment in a JSON format with a "safe" boolean and an optional "reason" string.
    Example safe output: {{"safe": true}}
    Example unsafe output: {{"safe": false, "reason": "Contains hate speech"}}
    """

    response = model.predict(prompt=prompt, temperature=0.2)

    # Basic parsing of the response assuming the model tries to return JSON
    # In a real-world scenario, robust JSON parsing and error handling would be needed.
    try:
        # Attempt to parse the response as JSON
        # Note: Gemini-pro might not always return perfect JSON directly,
        # so this is a simplified attempt.
        import json
        return json.loads(response.text.strip())
    except json.JSONDecodeError:
        # Fallback if the response is not clean JSON
        return {"safe": False, "reason": f"Could not parse safety assessment from AI: {response.text.strip()}"}

