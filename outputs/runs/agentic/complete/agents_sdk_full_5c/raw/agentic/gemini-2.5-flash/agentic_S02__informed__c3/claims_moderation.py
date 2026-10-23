import requests
import json
from identity_client import IdentityClientConfig

def moderate_text_claims(text_to_moderate: str) -> dict:
    if not IdentityClientConfig.AZURE_CONTENT_SAFETY_ENDPOINT or not IdentityClientConfig.AZURE_CONTENT_SAFETY_KEY:
        raise ValueError("Azure Content Safety endpoint and key must be set in IDENTITY_CLIENT_CONFIG")

    endpoint = f"{{IdentityClientConfig.AZURE_CONTENT_SAFETY_ENDPOINT}}/contentsafety/text:analyze?api-version=2023-04-30-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": IdentityClientConfig.AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text_to_moderate
    }

    response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    example_claim = "This user also mentioned some offensive language during registration and has a suspicious background."
    if IdentityClientConfig.AZURE_CONTENT_SAFETY_ENDPOINT and IdentityClientConfig.AZURE_CONTENT_SAFETY_KEY:
        print("--- Claims Moderation using Azure AI Content Safety ---")
        try:
            moderation_results = moderate_text_claims(example_claim)
            print("Moderation Results:")
            print(json.dumps(moderation_results, indent=2))
        except requests.exceptions.HTTPError as e:
            print(f"Error moderating claims: {e}")
            print(f"Response: {e.response.text}")
        except ValueError as e:
            print(e)
    else:
        print("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY not set. Cannot run Azure AI Content Safety example.")
