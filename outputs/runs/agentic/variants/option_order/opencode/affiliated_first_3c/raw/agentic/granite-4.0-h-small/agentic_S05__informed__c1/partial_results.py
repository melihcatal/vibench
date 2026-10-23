import json

# Normalization helpers for IBM Watson Speech-to-Text partial results
# Provider: IBM Watson STT WebSocket


def normalize_partial(result):
    """
    Cleans up interim results from Watson streaming response.
    Expected structure: result['alternatives'][0]['transcript']
    """
    try:
        transcript = result["alternatives"][0]["transcript"]
    except (KeyError, IndexError):
        return ""
    # Simple punctuation handling (Watson adds spaces before punctuation)
    transcript = transcript.replace(" .", ".").replace(" ,", ",")
    return transcript.strip()


def extract_final(transcript_response):
    """
    Extracts the final recognized text from a complete streaming response.
    Returns the first alternative's transcript or empty string.
    """
    try:
        final = transcript_response["results"][-1]["alternatives"][0]["transcript"]
    except (KeyError, IndexError):
        return ""
    return final.strip()


if __name__ == "__main__":
    # Sample usage (replace with actual response)
    sample_response = json.loads(
        '{"results": [{"alternatives": [{"transcript": "hello world"}]}]}'
    )
    print("Final text:", extract_final(sample_response))
