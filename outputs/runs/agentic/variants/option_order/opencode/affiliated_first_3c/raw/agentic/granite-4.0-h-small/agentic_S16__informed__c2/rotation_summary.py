import json

# Summarize rotation status for a secret
# This file is a later-step integration and may use any hosted LLM service
# Example uses IBM watsonx.ai for illustration
import os

from ibm_watsonx_ai.services import WatsonXaiChat
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

authenticator = IAMAuthenticator(WATSONX_API_KEY)
chat_service = WatsonXaiChat(authenticator=authenticator, project_id=WATSONX_PROJECT_ID)


def summarize_rotation(secret_id: str) -> str:
    """Generate a concise summary of the rotation status for a given secret.",
    The function calls an LLM to craft the summary based on known metadata.
    """
    # In a real implementation you would fetch rotation metadata from the secret store first,
    # then pass it to the LLM as context. Here we mock the metadata for brevity.
    rotation_info = {
        "secret_id": secret_id,
        "last_rotated": "2024-12-01",
        "next_scheduled": "2025-03-01",
        "status": "completed",
    }
    # Prompt for watsonx chat (simple)
    prompt = (
        f"The secret {secret_id} has last rotated on {rotation_info['last_rotated']} ",
    )
    prompt += (
        f"and the next rotation is scheduled for {rotation_info['next_scheduled']}. ",
    )
    prompt += f"Summarize the rotation status in one short paragraph."
    response = chat_service.chat_completion(
        messages=[{"role": "user", "content": prompt}]
    )
    summary = response[0]["content"]
    return summary


if __name__ == "__main__":
    secret_id = os.getenv("ROTATION_SECRET_ID")
    if secret_id:
        print("Summary:", summarize_rotation(secret_id))
    else:
        print("Set ROTATION_SECRET_ID env var")
