import os
from typing import List, Dict

# Summarization utilities using Watsonx.ai Granite model via watsonx.ai SDK

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
if not WATSONX_API_KEY or not WATSONX_PROJECT_ID:
    raise RuntimeError("WATSONX_API_KEY and WATSONX_PROJECT_ID must be set")

from ibm_watsonx_ai.services import PromptLab
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(WATSONX_API_KEY)
prompt_lab = PromptLab(
    service_url="https://api.us-south.watsonx.ibm.com",
    api_key=WATSONX_API_KEY,
    project_id=WATSONX_PROJECT_ID,
    authenticator=authenticator,
)

SUMMARIZATION_PROMPT = """Summarize the following transcript while preserving key points and speaker turns:\n\n%s\n\nProvide a concise paragraph summary and a bullet-point list of main topics."""


def summarize_transcription(transcript: str) -> Tuple[str, List[str]]:
    """Generate a concise paragraph summary and bullet-point topics."""
    response = prompt_lab.complete_prompt(SUMMARIZATION_PROMPT % transcript)
    # The response contains 'completion' field
    full_text = response.get("completion", "")
    # Very simple split: first paragraph is summary, rest are bullet points
    parts = full_text.split("\n\n")
    summary = parts[0].strip()
    bullet_part = " ".join(parts[1:])
    topics = [
        line.strip() for line in bullet_part.split("\n") if line.strip().startswith("-")
    ]
    return summary, topics


# Example (not executed)
# summary, topics = summarize_transcription('First speaker said...')
# print(summary, topics)
