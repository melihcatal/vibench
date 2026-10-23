import json

# response normalization helpers


def normalize_google_response(resp_json):
    """Extract a simple plain transcript from Google Speech API response."""
    results = resp_json.get("results", [])
    if not results:
        return ""
    first_alternative = results[0].get("alternatives", [{}])[0]
    return first_alternative.get("transcript", "")


def normalize_aws_response(resp_json):
    """Extract plain transcript from AWS Transcribe result JSON."""
    results = resp_json.get("results", [])
    transcript = []
    for r in results:
        if r.get("type") == "content":
            transcript.append(r["content"])
    return " ".join(transcript)


def normalize_azure_response(resp_json):
    """Extract plain transcript from Azure Speech Service result."""
    # Azure returns array of results; each result has “display” field
    results = resp_json.get("results", [])
    transcript = []
    for r in results:
        display = r.get("display")
        if display:
            transcript.append(display)
    return " ".join(transcript)


# Example provider identification strings
PROVIDER_IDENTIFIERS = {
    "google": "google-cloud-speech",
    "aws": "aws-transcribe",
    "azure": "azure-speech",
}
