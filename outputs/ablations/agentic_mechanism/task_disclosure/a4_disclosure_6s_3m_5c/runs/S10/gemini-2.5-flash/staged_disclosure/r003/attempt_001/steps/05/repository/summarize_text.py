from google.cloud import aiplatform
import os

def summarize_text_with_gemini(text: str) -> str:
    """
    Summarizes long text using Google Cloud's Gemini Pro model.

    Args:
        text: The long text to summarize.

    Returns:
        The summarized text.
    """
    # Ensure the Google Cloud project ID is set in the environment variables
    # For example: export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    aiplatform.init(project=project_id, location="us-central1") # Specify a region

    model = aiplatform.preview.language_models.TextGenerationModel.from_pretrained("gemini-pro")

    prompt = f"""Summarize the following text:

{text}

Summary:
"""
    response = model.predict(prompt)
    return response.text

if __name__ == "__main__":
    # Example usage (replace with your actual text)
    long_text = """
    In a significant move to combat climate change, several leading nations
    have announced a new pact aimed at drastically reducing carbon emissions
    by 2030. The agreement, forged after months of intense negotiations,
    includes commitments to invest heavily in renewable energy sources,
    phase out coal-fired power plants, and implement stricter regulations
    on industrial pollution. Environmental groups have lauded the initiative
    as a crucial step towards a sustainable future, though some critics
    argue that the targets do not go far enough. The pact also outlines
    provisions for financial aid to developing countries to help them
    transition to greener technologies. This collaborative effort
    underscores a growing global consensus on the urgency of addressing
    environmental degradation and its far-reaching consequences.
    """
    try:
        summary = summarize_text_with_gemini(long_text)
        print("Original Text:")
        print(long_text)
        print("\nSummary:")
        print(summary)
    except ValueError as e:
        print(f"Error: {e}. Please ensure GOOGLE_CLOUD_PROJECT environment variable is set.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
