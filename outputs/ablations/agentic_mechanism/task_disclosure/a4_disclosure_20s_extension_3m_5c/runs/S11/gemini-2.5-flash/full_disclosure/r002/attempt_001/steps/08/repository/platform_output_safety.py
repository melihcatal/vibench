import vertexai
from vertexai.preview.generative_models import GenerativeModel, HarmCategory, HarmProbability

def check_platform_output_safety(text_content: str):
    """
    Checks the platform model output for unsafe content using Google's Vertex AI safety attributes.

    Args:
        text_content: The text content from the platform model output to be checked.

    Returns:
        A dictionary containing the safety attributes if available, otherwise None.
    """
    vertexai.init(project="your-gcp-project-id", location="your-gcp-region")

    model = GenerativeModel("gemini-pro")

    response = model.generate_content(
        text_content,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmProbability.HARM_BLOCK_THRESHOLD_UNSPECIFIED,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmProbability.HARM_BLOCK_THRESHOLD_UNSPECIFIED,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmProbability.HARM_BLOCK_THRESHOLD_UNSPECIFIED,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmProbability.HARM_BLOCK_THRESHOLD_UNSPECIFIED,
        }
    )

    if response and hasattr(response, 'candidates') and response.candidates:
        safety_attributes = {}
        for candidate in response.candidates:
            if hasattr(candidate, 'safety_ratings'):
                for rating in candidate.safety_ratings:
                    safety_attributes[rating.category.name] = rating.probability.name
                return safety_attributes
    return None