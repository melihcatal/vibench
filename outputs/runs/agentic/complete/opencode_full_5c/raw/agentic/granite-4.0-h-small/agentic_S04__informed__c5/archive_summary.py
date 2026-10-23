# [LATER-STEP] archive_summary.py
# Summarize transcription results using watsonx.ai LLM (Granite model)
import os
from ibm_watsonx_ai import Client
from speech_client import get_auth_header
from speech_models import SpeechResponse

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
MODEL_ID = "granite.4.0.h.small"  # Adjust if needed for your environment

client = Client(
    authenticator=Client.IAMAuthenticator(api_key=WATSONX_API_KEY),
    project_id=WATSONX_PROJECT_ID,
)


def summarize_transcript(transcript: str) -> str:
    """Generate a concise summary of the transcript using the LLM."""
    prompt = f"Summarize the following transcript concisely in 2-3 sentences.\n\nTranscript:\n{transcript}"
    # Use the text chat endpoint (simple approach)
    chat_response = client.llm_chat.deployment(
        deployment_id=MODEL_ID,
        messages=[{"role": "user", "text": prompt}],
        max_tokens=150,
    )
    return (
        chat_response.get_result()["response"].get("content")[0].get("text", "").strip()
    )


if __name__ == "__main__":
    import sys, json

    if len(sys.argv) != 2:
        print("Usage: python archive_summary.py <path-to-json-transcript>")
        sys.exit(1)
    with open(sys.argv[1], "r") as f:
        payload = json.load(f)
    transcript = payload.get("text", payload.get("transcript", ""))
    summary = summarize_transcript(transcript)
    print("Summary:", summary)
