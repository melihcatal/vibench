import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def summarize_asset_content(content: str) -> str:
    """Summarizes content extracted from a stored asset using Google's Gemini Pro model."""
    vertexai.init(project="your-gcp-project-id", location="us-central1") # Replace with your GCP project ID
    model = GenerativeModel("gemini-pro")
    
    prompt = f"Summarize the following content:

{content}"
    response = model.generate_content(prompt)
    
    return response.text

if __name__ == "__main__":
    # Example usage: Replace with actual content extracted from a stored asset
    sample_content = """
    The quick brown fox jumps over the lazy dog. This is a classic pangram, a sentence
    that contains every letter of the alphabet at least once. Pangrams are often used
    to display typefaces or to test typing skills. Another popular pangram is
    "Pack my box with five dozen liquor jugs."
    """
    summary = summarize_asset_content(sample_content)
    print("Summary:", summary)
