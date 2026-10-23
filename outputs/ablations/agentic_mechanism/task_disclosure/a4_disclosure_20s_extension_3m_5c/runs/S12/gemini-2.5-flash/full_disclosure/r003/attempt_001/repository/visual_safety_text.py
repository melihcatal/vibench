from google.cloud import aiplatform
import vertexai
from vertexai.preview.generative_models import GenerativeModel, HarmCategory, HarmBlockThreshold

def check_unsafe_text(text: str) -> dict:
    """
    Checks the given text for unsafe content using Google Cloud's Vertex AI Generative Model.

    Args:
        text: The text to be checked for unsafe content.

    Returns:
        A dictionary containing the safety attributes of the text.
    """
    # Initialize Vertex AI with your Google Cloud project details
    # Replace 'your-project-id' and 'your-region' with your actual project ID and region
    vertexai.init(project="your-project-id", location="your-region")

    model = GenerativeModel("gemini-pro")

    # Configure safety settings to block content at certain thresholds
    safety_settings = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }

    response = model.generate_content(
        text,
        safety_settings=safety_settings,
        generation_config={"max_output_tokens": 1} # We only care about safety attributes, not generated text
    )

    safety_attributes = {}
    if response.prompt_feedback and response.prompt_feedback.safety_attributes:
        for category, probability in response.prompt_feedback.safety_attributes.categories_and_probabilities.items():
            safety_attributes[category.name] = probability
        safety_attributes["blocked"] = response.prompt_feedback.blocked

    return safety_attributes
