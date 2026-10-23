import os
from google.cloud import aiplatform
from google.generativeai.types import HarmCategory, HarmBlockThreshold

def summarize_asset_content(text_content: str) -> str:
    """
    Summarizes content extracted from a stored asset using Google Cloud's Generative AI.

    Args:
        text_content: The text content extracted from the asset.

    Returns:
        A summarized version of the text content.
    """
    # Initialize the AI Platform client.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # authenticate using `gcloud auth application-default login`
    # Replace 'your-project-id' and 'your-location' with your Google Cloud project details.
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    aiplatform.init(project=project_id, location=location)

    # Use the GenerativeModel class for Gemini Pro
    model = aiplatform.preview.generative_models.GenerativeModel("gemini-pro")

    prompt = f"Please provide a concise summary of the following text:

{text_content}"

    response = model.generate_content(
        prompt,
        generation_config={
            "max_output_tokens": 500,  # Limit summary length
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40
        },
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }
    )

    return response.text.strip()
