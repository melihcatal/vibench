import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def check_caption_safety(text: str, project_id: str = None, location: str = "us-central1") -> dict:
    """Checks live transcript text for unsafe content using Vertex AI's generative models.

    Args:
        text: The transcript text to check.
        project_id: Your Google Cloud project ID. If None, it will be inferred.
        location: The Google Cloud region for Vertex AI.

    Returns:
        A dictionary with safety attributes (e.g., categories and scores).
    """
    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Google Cloud project ID must be provided or set in GOOGLE_CLOUD_PROJECT env var.")

    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro")

    # The safety attributes are usually returned with the response content automatically
    # when using models like gemini-pro. We can craft a prompt to explicitly ask for a safety assessment.
    prompt = f"Analyze the following text for safety attributes (toxicity, harassment, hate speech, dangerous content, sexual content, violent content) and provide a safety score or categorization. Return a JSON object with safety categories and their likelihood/score: ''{text}''"

    response = model.generate_content([prompt])

    # The safety attributes are typically part of the response object itself if the API supports it,
    # or we interpret the model's textual response.
    # For this example, we'll look for the safety_attributes in the first candidate's content.
    safety_attributes = {}
    if response.candidates:
        for safety_rating in response.candidates[0].safety_ratings:
            safety_attributes[safety_rating.category.name] = safety_rating.probability.name

    print(f"Safety check for '{text}': {safety_attributes}")
    return safety_attributes
