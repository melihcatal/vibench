import os
import requests
import json


def moderate_text_claims(text: str) -> Dict[str, Any]:
    """Moderates free-text claims or notes using Azure AI Content Safety."""
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not all([endpoint, key]):
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    api_version = "2023-10-15-preview"  # Use a specific API version
    url = f"{endpoint}content:analyze?api-version={api_version}"

    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    body = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()  # Raise an exception for HTTP errors

    return response.json()


# Example usage (not part of the file, just for demonstration):
# if __name__ == "__main__":
#     os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"] = "https://YOUR_RESOURCE_NAME.cognitiveservices.azure.com/contentsafety/"
#     os.environ["AZURE_CONTENT_SAFETY_KEY"] = "YOUR_AZURE_CONTENT_SAFETY_KEY"
#     sample_claim_text = "I really hate this new policy, it's so bad and unfair."
#     try:
#         moderation_result = moderate_text_claims(sample_claim_text)
#         print("Moderation Result:")
#         print(json.dumps(moderation_result, indent=2))
#     except requests.exceptions.HTTPError as e:
#         print(f"Error moderating text: {e.response.text}")
#     except ValueError as e:
#         print(f"Configuration Error: {e}")
#     except Exception as e:
#         print(f"An error occurred: {e}")
