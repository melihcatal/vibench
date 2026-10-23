import os
from google.cloud import aiplatform

def summarize_moderation_decisions(moderation_results: list[dict]) -> str:
    """
    Summarizes moderation decisions using Google Cloud Vertex AI's Generative Model.
    
    Args:
        moderation_results (list[dict]): A list of moderation decision dictionaries.
                                       Each dict could contain info like {"text": "...", "is_allowed": True/False, "reasons": [...]}
                                       
    Returns:
        str: A summary of the moderation decisions.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")

    aiplatform.init(project=project_id, location=location)

    # Using a text-bison model for summarization
    # The exact model ID might vary or be updated, 'text-bison@001' is a common choice.
    model = aiplatform.PreviewModel.from_pretrained("gemini-pro") # Using gemini-pro for better performance

    prompt_parts = [
        "Given the following moderation results, summarize the key findings and decisions:",
        "\n\nModeration Results:",
        str(moderation_results),
        "\n\nSummary:",
    ]
    
    response = model.predict(prompt=prompt_parts)
    return response.text
