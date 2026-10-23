import vertexai
from vertexai.generative_models import GenerativeModel, Part, HarmCategory, HarmBlockThreshold
import os

def check_message_safety(message_text: str) -> dict:
    """Checks message payload text for unsafe content using Google Cloud's Gemini Pro model."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1") # e.g., us-central1

    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro") # Using the Gemini Pro model

    # Define safety settings to evaluate different harm categories
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

    response = model.generate_content(
        message_text,
        safety_settings=safety_settings
    )

    safety_attributes = {}
    if response.candidates and response.candidates[0].safety_ratings:
        for rating in response.candidates[0].safety_ratings:
            safety_attributes[rating.category.name] = {
                "score": rating.score.name,
                "blocked": rating.blocked
            }
    
    # Also check for prompt feedback if any safety concerns blocked the response generation itself
    if response.prompt_feedback and response.prompt_feedback.safety_ratings:
        print("Note: Prompt feedback available, some content might have been blocked.")
        for rating in response.prompt_feedback.safety_ratings:
             safety_attributes[rating.category.name] = {
                "score": rating.score.name,
                "blocked": rating.blocked
            }

    return safety_attributes

if __name__ == "__main__":
    safe_message = "Hello, how are you doing today? I hope everything is fine."
    unsafe_message = "I hate you, you are worthless and should disappear!" # Example of potentially unsafe content

    print("Checking safe message:")
    safe_result = check_message_safety(safe_message)
    print(safe_result)

    print("\nChecking unsafe message:")
    unsafe_result = check_message_safety(unsafe_message)
    print(unsafe_result)
