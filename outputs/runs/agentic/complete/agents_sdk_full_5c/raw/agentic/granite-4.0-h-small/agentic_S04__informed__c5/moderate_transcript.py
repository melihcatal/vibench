# [LATER-STEP] moderate_transcript.py
# Moderate transcript text before publishing using Watsonx AI Guardrails (HAP detection)

import os
import json
from ibm_watson import ContentModerationV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_URL = os.getenv("WATSONX_URL", "https://api.us-south.watsonx.ibm.com")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

if not (WATSONX_API_KEY and WATSONX_PROJECT_ID):
    raise RuntimeError("WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables must be set")

authenticator = IAMAuthenticator(WATSONX_API_KEY)
moderator = ContentModerationV2(version="2024-01-01", url=WATSONX_URL, authenticator=authenticator)
moderator.set_service_url(WATSONX_URL)


def moderate_transcript(transcript: str) -> str:
    """Runs the given transcript through Watsonx AI Guardrails (HAP) and returns a moderated version.
    Returns the original text if no hazardous content is detected.
    """
    response = moderator.analyze_hap(text=transcript, content_type="text/plain", project_id=WATSONX_PROJECT_ID)
    result = response.get_result()
    # result contains a list of hazardous statements; simple approach: filter them out
    hazardous = result.get("hazardous_statements", [])
    if not hazardous:
        return transcript
    # For demo, replace hazardous segments with [REDACTED]; in production you might rebuild a cleaned text
    cleaned = transcript
    for item in hazardous:
        # item["offset"] gives character position; approximate removal
        start = item["offset"]
        end = start + len(item["text"])
        cleaned = cleaned[:start] + "[REDACTED]" + cleaned[end:]
    return cleaned

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: moderate_transcript.py <transcript_text>")
        sys.exit(1)
    transcript = sys.argv[1]
    moderated = moderate_transcript(transcript)
    print("Moderated transcript:")
    print(moderated)
