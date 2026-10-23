import vertexai
from vertexai.generative_models import GenerativeModel, Part
import os

def summarize_message_content(message_text: str) -> str:
    """Summarizes the content of a message using Google Cloud's Gemini Pro model."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1") # e.g., us-central1

    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro") # Using the Gemini Pro model

    prompt = f"Summarize the following message content concisely:

{message_text}"

    response = model.generate_content(prompt)
    if response.candidates and response.candidates[0].content:
        # Assuming the first part is the summary text
        summary = "".join([part.text for part in response.candidates[0].content.parts])
        return summary
    return "Could not generate summary."

if __name__ == "__main__":
    sample_message = """
    Customer support ticket opened for order #XYZ-789.
    The customer reported receiving a damaged item, specifically a "Vintage Ceramic Vase".
    They attached photos of the damage.
    Requested a full refund or a replacement.
    Agent needs to review the photos and initiate the return process.
    """
    print("Original message:
", sample_message)
    summary = summarize_message_content(sample_message)
    print("\nSummary:\n", summary)
