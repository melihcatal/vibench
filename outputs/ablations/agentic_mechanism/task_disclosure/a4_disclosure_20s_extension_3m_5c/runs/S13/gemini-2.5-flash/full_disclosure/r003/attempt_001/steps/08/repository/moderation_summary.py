import os
from google.cloud import aiplatform

def summarize_moderation_decisions(decisions: list[dict]) -> str:
    """
    Summarizes moderation decisions using Google Cloud's Vertex AI.

    Args:
        decisions: A list of dictionaries, where each dictionary represents a moderation decision.
                   Each dictionary is expected to have a "text" field with the content to summarize.

    Returns:
        A string containing the summary of the moderation decisions.
    """
    # Initialize Vertex AI client
    aiplatform.init(project=os.environ.get("GCP_PROJECT_ID"), location=os.environ.get("GCP_LOCATION"))

    # Load the text model (e.g., Gemini-Pro)
    # The model identifier is a provider-specific signal.
    model = aiplatform.GenerativeModel("gemini-pro")

    # Combine decisions into a single prompt for summarization
    decision_texts = [f"Decision {i+1}: {d.get("text", "")}" for i, d in enumerate(decisions)]
    prompt = "Summarize the following moderation decisions:
" + "\n".join(decision_texts)

    # Generate the summary
    response = model.generate_content(prompt)

    return response.text

