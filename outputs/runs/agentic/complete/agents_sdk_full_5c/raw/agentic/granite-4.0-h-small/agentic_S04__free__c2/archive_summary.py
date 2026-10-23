import os
import requests
from typing import List, Dict

# Assume Azure Cognitive Services Text Analytics for Good (Summarization)
SUMMARY_ENDPOINT = "https://<your-resource-name>.cognitiveservices.azure.com"
SUMMARY_KEY = os.getenv("AZURE_SUMMARIZATION_KEY")
SUMMARY_VERSION = "2023-04-01"

#
# Summarize transcription results
def archive_summary(transcript: str) -> Dict[str, Any]:
    """Call Azure Summarization API to produce a concise summary of the transcript.",
    Returns the JSON payload returned by the service (including summary text).
    """
    path = "/text/analytics/v3.2/summarization/extractive"
    url = f"{SUMMARY_ENDPOINT}{path}"
    headers = {
        "Ocp-Apim-Subscription-Key": SUMMARY_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "documents": [
            {
                "id": "1",
                "text": transcript,
            }
        ],
        "parameters": {
            "sentenceCount": 5,
        },
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

# Export only the summarizer helper
__all__ = ["archive_summary"]
