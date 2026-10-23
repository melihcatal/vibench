from google.cloud import aiplatform
from google.generativeai.types import HarmCategory, HarmBlockThreshold

def check_safety(text: str) -> dict:
    """
    Checks the given text for unsafe content using Google's Generative AI safety features.

    Args:
        text: The text to be checked for safety.

    Returns:
        A dictionary containing safety attributes and ratings.
    """
    model = aiplatform.init(project="YOUR_PROJECT_ID", location="YOUR_REGION")
    # Using a specific model, e.g., "gemini-pro"
    # Ensure that "gemini-pro" is enabled for your project and region
    safety_settings = [
        {"category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE},
        {"category": HarmCategory.HARM_CATEGORY_HATE_SPEECH, "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE},
        {"category": HarmCategory.HARM_CATEGORY_HARASSMENT, "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE},
        {"category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE},
    ]

    # In a real application, you would interact with the model here
    # For demonstration, we'll return a mock safety response
    mock_safety_response = {
        "text_input": text,
        "safety_ratings": [
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "probability": "NEGLIGIBLE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "probability": "NEGLIGIBLE"},
            {"category": "HARM_CATEGORY_HARASSMENT", "probability": "NEGLIGIBLE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "probability": "NEGLIGIBLE"},
        ],
        "blocked": False
    }
    return mock_safety_response

if __name__ == "__main__":
    test_text = "This is a test prompt."
    safety_result = check_safety(test_text)
    print(safety_result)
