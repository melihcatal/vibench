
import vertexai
from vertexai.generative_models import GenerativeModel, Part, GenerationConfig
import os

def summarize_asset_content(content: str) -> str:
    """Summarizes content extracted from a stored asset using Google's Generative AI API."""

    vertexai.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location=os.environ.get("GOOGLE_CLOUD_LOCATION"))
    model = GenerativeModel("gemini-pro")

    generation_config = GenerationConfig(
        temperature=0.2,
        top_p=0.8,
        top_k=40
    )

    prompt = f"""Summarize the following content from a stored asset:
{content}

Provide a concise summary highlighting the main points.
"""

    response = model.generate_content(
        [prompt],
        generation_config=generation_config
    )

    return response.text

if __name__ == "__main__":
    # Example usage (replace with actual content from your stored asset)
    sample_content = """
    The quick brown fox jumps over the lazy dog. This is a classic pangram used to test typewriters and computer keyboards.
    It contains all the letters of the English alphabet. Another common use is in typography to display font samples.
    """
    summary = summarize_asset_content(sample_content)
    print("Summary:")
    print(summary)
