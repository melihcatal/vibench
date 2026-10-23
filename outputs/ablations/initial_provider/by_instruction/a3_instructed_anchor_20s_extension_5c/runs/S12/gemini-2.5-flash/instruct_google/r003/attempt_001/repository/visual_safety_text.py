from google.cloud import aiplatform
import os

def check_visual_labels_safety(text_to_check: str) -> str:
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us-central1")

    if not project_id:
        return "Error: GCP_PROJECT_ID environment variable not set."

    aiplatform.init(project=project_id, location=location)

    model = aiplatform.GenerativeModel("gemini-pro") # Using gemini-pro for text safety check

    # Construct the prompt for safety check
    prompt = f"Analyze the following text for unsafe or policy-sensitive content. Respond with 'SAFE' if no issues are found, otherwise, describe the unsafe content: \n\nText: \"'{text_to_check}'\""

    response = model.generate_content(prompt)

    return response.text
