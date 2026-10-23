import os
import requests
from safety_client import get_azure_content_safety_client
from safety_models import ContentSafetyResponse

def moderate_text(text: str) -> ContentSafetyResponse:
    """Scores user text for unsafe or policy-violating content using Azure AI Content Safety."""
    client = get_azure_content_safety_client()
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety endpoint and key must be set as environment variables.")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return ContentSafetyResponse(
            hate_severity=next((c["severity"] for c in result["categoriesAnalysis"] if c["category"] == "Hate"), 0),
            self_harm_severity=next((c["severity"] for c in result["categoriesAnalysis"] if c["category"] == "SelfHarm"), 0),
            sexual_severity=next((c["severity"] for c in result["categoriesAnalysis"] if c["category"] == "Sexual"), 0),
            violence_severity=next((c["severity"] for c in result["categoriesAnalysis"] if c["category"] == "Violence"), 0)
        )
    except requests.exceptions.RequestException as e:
        print(f"Error calling Azure Content Safety API: {e}")
        raise

if __name__ == "__main__":
    # Example usage (requires environment variables AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY)
    # os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"] = "YOUR_ENDPOINT"
    # os.environ["AZURE_CONTENT_SAFETY_KEY"] = "YOUR_KEY"
    # test_text = "I will hurt everyone."
    # moderation_result = moderate_text(test_text)
    # print(f"Moderation result for '{test_text}': {moderation_result.to_dict()}")
    pass
