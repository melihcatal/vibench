import os
from google.cloud import aiplatform
from google.generativeai import GenerativeModel

def summarize_asset_content(content: str) -> str:
    """
    Summarizes content extracted from a stored asset using Google's Generative AI.

    Args:
        content: The text content to be summarized.

    Returns:
        A summarized version of the content.
    """
    # Initialize Google Cloud AI Platform (ensure PROJECT_ID and LOCATION are set as environment variables)
    # For example:
    # export GOOGLE_CLOUD_PROJECT=your-gcp-project-id
    # export GOOGLE_CLOUD_LOCATION=us-central1
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION")

    if not project_id or not location:
        raise ValueError("Environment variables GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION must be set.")

    aiplatform.init(project=project_id, location=location)

    # Use the GenerativeModel class from google.generativeai for text generation
    # The 'gemini-pro' model is a concrete identifier for the provider.
    model = GenerativeModel("gemini-pro")

    prompt = f"Summarize the following content:

{content}"

    response = model.generate_content(prompt)
    return response.text.strip()

if __name__ == "__main__":
    # Example usage:
    # In a real scenario, 'asset_content' would be loaded from a stored asset (e.g., a file, database, cloud storage).
    example_content = """
    The quick brown fox jumps over the lazy dog. This is a classic pangram often used to test typewriters and computer keyboards.
    It uses every letter of the English alphabet at least once. Pangrams are useful for displaying fonts and testing equipment.
    Another example of a pangram is "Pack my box with five dozen liquor jugs."
    """
    summary = summarize_asset_content(example_content)
    print("Original Content:")
    print(example_content)
    print("
Summarized Content:")
    print(summary)
