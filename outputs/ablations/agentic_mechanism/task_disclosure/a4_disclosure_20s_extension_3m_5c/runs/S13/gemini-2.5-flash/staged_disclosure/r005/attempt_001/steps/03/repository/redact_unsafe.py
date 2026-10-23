import os
from google import genai
from google.genai.types import (
    GenerateContentConfig,
    HarmBlockThreshold,
    HarmCategory,
    SafetySetting,
)

def redact_unsafe_text(text: str, project_id: str, location: str) -> str:
    """
    Flags or redacts unsafe spans from text using Google Gemini's safety features.

    Args:
        text: The input text to be moderated.
        project_id: The Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").

    Returns:
        The original text if safe, or a message indicating redaction if unsafe content is detected.
    """
    # Initialize the Vertex AI client for Generative AI
    # This assumes that the GOOGLE_API_KEY environment variable is set or
    # application default credentials are configured.
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    client = genai.Client()

    # Configure safety settings to block content at a low threshold for all categories
    safety_settings = [
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_UNSPECIFIED,
            threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
    ]

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",  # Using a concrete Gemini model
            contents=text,
            config=GenerateContentConfig(
                safety_settings=safety_settings,
            ),
        )

        if response.candidates and response.candidates[0].finish_reason == genai.types.FinishReason.SAFETY:
            blocked_categories = []
            for rating in response.candidates[0].safety_ratings:
                if rating.blocked:
                    blocked_categories.append(str(rating.category).replace("HARM_CATEGORY_", ""))
            return f"Content redacted due to unsafe content in categories: {", ".join(blocked_categories)}"
        elif response.text:
            return response.text
        else:
            return "Unable to process content or empty response."

    except Exception as e:
        return f"Error during content moderation: {e}"

if __name__ == "__main__":
    # Example Usage (replace with your actual project_id and location)
    # Ensure you have authenticated to Google Cloud and set up your GOOGLE_API_KEY
    # For example: export GOOGLE_API_KEY="YOUR_API_KEY"
    
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") # Or specify your project ID
    location = "us-central1" # Or specify your region

    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
        exit()

    if not os.environ.get("GOOGLE_API_KEY"):
        print("Please set the GOOGLE_API_KEY environment variable with your Gemini API key.")
        exit()

    unsafe_text = "I hate you, you are a terrible person!"
    safe_text = "Hello, how are you today?"

    print(f"Original unsafe text: {unsafe_text}")
    redacted_output = redact_unsafe_text(unsafe_text, project_id, location)
    print(f"Redacted output: {redacted_output}\n")

    print(f"Original safe text: {safe_text}")
    safe_output = redact_unsafe_text(safe_text, project_id, location)
    print(f"Safe output: {safe_output}")
