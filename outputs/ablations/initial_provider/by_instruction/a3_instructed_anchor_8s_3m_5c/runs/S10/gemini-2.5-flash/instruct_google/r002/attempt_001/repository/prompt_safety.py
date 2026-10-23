import os
from google.cloud import aiplatform
from google.generativeai import GenerativeModel, configure
from google.generativeai.types import HarmCategory, HarmBlockThreshold

def check_safety(text: str) -> dict:
    """
    Checks the given text for unsafe content using Google Generative AI's safety features.
    Returns a dictionary indicating safety attributes.
    """
    # Configure the Google Generative AI client
    # configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # For Vertex AI:
    # aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location=os.environ.get("GOOGLE_CLOUD_LOCATION"))
    # model = GenerativeModel(model_name="gemini-pro")

    # For Gemini API
    model = GenerativeModel(model_name="gemini-pro")

    # The safety settings are typically applied during content generation.
    # For checking arbitrary text, we can attempt to generate a simple response
    # and inspect the safety attributes if the model blocks the content.
    # This is a conceptual example, as direct 'safety check' API might differ.
    try:
        response = model.generate_content(
            text,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )
        # If the response is blocked, safety_ratings will be present
        if response.prompt_feedback and response.prompt_feedback.safety_ratings:
            return {rating.category.name: rating.probability.name for rating in response.prompt_feedback.safety_ratings}
        return {"status": "safe"}
    except Exception as e:
        # If an exception occurs due to safety settings, it indicates unsafe content
        return {"status": "unsafe", "details": str(e)}

