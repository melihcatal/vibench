import requests

# Perspective API (Google) for prompt safety checking
# Set your API key in the environment variable PERSPECTIVE_API_KEY

PERSPECTIVE_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def is_prompt_safe(prompt: str, threshold: float = 0.5) -> bool:
    """Check a prompt (or generated text) for toxicity using Perspective API."""
    if "PERSPECTIVE_API_KEY" not in os.environ:
        raise RuntimeError("Set PERSPECTIVE_API_KEY environment variable.")
    payload = {
        "comment": {"text": prompt},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    headers = {
        "x-api-key": os.environ["PERSPECTIVE_API_KEY"],
        "content-type": "application/json",
    }
    response = requests.post(PERSPECTIVE_ENDPOINT, json=payload, headers=headers)
    result = response.json()
    score = (
        result["attributeScores"]
        .get("TOXICITY", {})
        .get("summaryScore", {})
        .get("value", 0.0)
    )
    return score < threshold


# Example usage
# if __name__ == "__main__":
#     text = "user input"
#     print(f"Prompt safe? {is_prompt_safe(text)}")
