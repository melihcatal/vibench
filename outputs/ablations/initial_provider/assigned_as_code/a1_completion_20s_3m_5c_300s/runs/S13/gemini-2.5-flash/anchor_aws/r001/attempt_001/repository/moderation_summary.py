import os
from typing import List, Dict, Any
from google.cloud import aiplatform
from safety_models import ModerationDecision

def moderation_summary(decisions: List[ModerationDecision], config: Dict[str, Any] = None) -> str:
    config = config or {}
    
    # Initialize Vertex AI
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or authenticated otherwise
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", config.get("google_cloud_project"))
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", config.get("google_cloud_location", "us-central1"))

    if not project_id:
        raise ValueError("Google Cloud Project ID not provided. Set GOOGLE_CLOUD_PROJECT env var or pass in config.")

    aiplatform.init(project=project_id, location=location)

    # Use the GenerativeModel class for Gemini Pro
    model = aiplatform.preview.generative_models.GenerativeModel("gemini-pro")

    summary_prompt = """Summarize the following moderation decisions. Highlight any patterns, common reasons for flags, and overall safety status.

Moderation Decisions:
"""
    for i, decision in enumerate(decisions):
        summary_prompt += f"\nDecision {i+1}:\n"
        summary_prompt += f"  Text: {decision.text}\n"
        summary_prompt += f"  Is Safe: {decision.is_safe}\n"
        summary_prompt += f"  Reasons: {', '.join(decision.reasons) if decision.reasons else 'N/A'}\n"
        summary_prompt += f"  Scores: {decision.scores}\n"

    response = model.generate_content(summary_prompt)
    return response.text
