import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def summarize_moderation_decisions(decisions: list[dict]) -> str:
    """
    Summarizes moderation decisions using Google Cloud's Generative AI.

    Args:
        decisions: A list of dictionaries, where each dictionary represents a
                   moderation decision.

    Returns:
        A string containing the summary of moderation decisions.
    """
    vertexai.init(project="your-gcp-project-id", location="us-central1") # Replace with your GCP project ID and region
    model = GenerativeModel("gemini-pro") # Using gemini-pro for summarization

    decisions_text = "\n".join([str(d) for d in decisions])
    prompt = f"Summarize the following moderation decisions:\n{decisions_text}"

    response = model.generate_content(prompt)
    return response.text

