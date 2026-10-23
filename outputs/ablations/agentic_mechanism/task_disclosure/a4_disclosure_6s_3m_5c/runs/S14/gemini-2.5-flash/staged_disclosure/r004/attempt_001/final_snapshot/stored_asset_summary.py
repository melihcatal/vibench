from google.cloud import aiplatform
import os

def summarize_asset_content(content: str) -> str:
    """Summarizes content extracted from a stored asset using Google Cloud Vertex AI.

    Args:
        content: The text content to summarize.

    Returns:
        A summarized version of the content.
    """
    # Initialize Vertex AI
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # authenticate using `gcloud auth application-default login`
    aiplatform.init(project=os.getenv("GOOGLE_CLOUD_PROJECT"), location=os.getenv("GOOGLE_CLOUD_REGION", "us-central1"))

    # Use a specific generative model for summarization
    model = aiplatform.preview.generative_models.GenerativeModel("gemini-pro")

    prompt = f"Summarize the following content concisely:

{content}"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error during summarization: {e}"

if __name__ == '__main__':
    # Example usage:
    # In a real scenario, content would be extracted from a stored asset (e.g., GCS, S3, etc.)
    sample_content = """
    The quick brown fox jumps over the lazy dog. This sentence is a well-known pangram,
    meaning it contains every letter of the alphabet at least once. Pangrams are often
    used to display typefaces or for testing purposes in various computing contexts.
    They are also a fun linguistic curiosity. There are many other pangrams in English,
    but this one is arguably the most famous.
    """
    summarized_text = summarize_asset_content(sample_content)
    print("Original Content:")
    print(sample_content)
    print("\nSummarized Content:")
    print(summarized_text)
