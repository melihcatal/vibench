# LATER-STEP implementation - Summarizes transcription results using Granite model via watsonx.ai

import os
from ibm_watsonx_ai import watsonx
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Provider identifier
PROVIDER = "IBM Granite via watsonx.ai"

# Load API key and project ID from environment variables
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Authenticate and create a chat completion client
authenticator = IAMAuthenticator(WATSONX_API_KEY)
client = watsonx(base_url="https://api.us-south.watsonx.ibm.com")
client.set_authenticator(authenticator)

# Use the Granite 4.0 (h) model for summarization
model_id = "granite-4.0-h"


def archive_summary(transcript_segments):
    """Generates a concise summary of all transcription segments using a hosted LLM.

    Args:
        transcript_segments (list): List of strings, each a segment of the full transcript.

    Returns:
        dict: Contains a summary and metadata about the summarization process.
    """
    prompt = f"Summarize the following transcript in three bullet points. Preserve key topics and timings.\n\n{'\n'.join(transcript_segments)}"
    response = client.chat_completion(
        model=model_id, messages=[{"role": "user", "content": prompt}], max_tokens=200
    )
    summary = response.get("choices", [{}])[0].get("message", {}).get("content", "")
    return {"provider": PROVIDER, "model": model_id, "summary": summary.strip()}
