import os
from typing import Dict, Any
from google.cloud import aiplatform

def summarize_moderation_decisions(decisions: List[Dict[str, Any]], project_id: str, location: str = "us-central1") -> str:
    """Summarize moderation decisions using Google Cloud Vertex AI's Gemini Pro model."""

    aiplatform.init(project=project_id, location=location)
    
    # Use a specific model that supports summarization, e.g., gemini-pro
    # Ensure the model ID is correct for your region and project setup.
    model_name = "gemini-pro"
    model = aiplatform.preview.language_models.ChatModel.from_pretrained(model_name)

    # Construct a prompt for summarization
    prompt_text = "Summarize the following moderation decisions:\n\n"
    for decision in decisions:
        prompt_text += f"Message ID: {decision.get('message_id', 'N/A')}\n"
        prompt_text += f"Is Safe: {decision.get('is_safe', 'N/A')}\n"
        prompt_text += f"Moderation Results: {decision.get('moderation_results', 'N/A')}\n\n"

    response = model.predict(prompt_text)
    return response.text
