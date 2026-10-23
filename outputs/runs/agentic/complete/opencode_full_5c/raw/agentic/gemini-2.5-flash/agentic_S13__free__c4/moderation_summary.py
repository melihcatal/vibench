import os
from typing import Dict, List
import vertexai  # Provider identifiable import
from vertexai.preview.generative_models import GenerativeModel, Part, Image


def summarize_moderation_decisions(
    moderation_results: List[Dict], project_id: str, location: str = "us-central1"
) -> str:
    """Summarizes moderation decisions using Google Cloud's Generative AI model.

    Args:
        moderation_results: A list of dictionaries, where each dictionary contains moderation scores for a text.
        project_id: The Google Cloud project ID.
        location: The Google Cloud location for Vertex AI.

    Returns:
        A summary of the moderation decisions.
    """
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-1.5-flash-001")  # Concrete model identifier

    prompt_parts = [
        "You are an AI assistant that summarizes moderation decisions.\n",
        "Here are the moderation results:",
        str(moderation_results),  # Convert the list of dicts to a string for the prompt
        "Please provide a concise summary of these moderation decisions, highlighting any trends or significant findings.",
    ]

    response = model.generate_content(prompt_parts)
    return response.text


if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    if project_id == "your-gcp-project-id":
        print(
            "Please set the GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id' with your actual project ID."
        )
    else:
        # Example moderation results (similar to what moderate_batch.py might return)
        mock_moderation_results = [
            {
                "text": "I love this product!",
                "scores": {"TOXICITY": 0.05, "SEXUAL": 0.01, "THREAT": 0.00},
            },
            {
                "text": "You are an idiot.",
                "scores": {"TOXICITY": 0.9, "SEXUAL": 0.02, "THREAT": 0.1},
            },
            {
                "text": "Let's go for a walk.",
                "scores": {"TOXICITY": 0.01, "SEXUAL": 0.00, "THREAT": 0.00},
            },
            {
                "text": "Kill yourself!",
                "scores": {"TOXICITY": 0.95, "SEXUAL": 0.05, "THREAT": 0.85},
            },
        ]

        summary = summarize_moderation_decisions(mock_moderation_results, project_id)
        print("\nModeration Summary:")
        print(summary)
