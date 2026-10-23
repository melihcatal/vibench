import os
import requests
import json

def moderate_profile_text(text: str) -> dict:
    """
    Moderates profile text before account activation using Azure AI Content Safety.
    Requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise EnvironmentError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY "
            "environment variables must be set."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "outputType": "FourSeverityLevels"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}
    except json.JSONDecodeError as e:
        return {"error": f"Failed to decode JSON response: {e}, Response: {response.text}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage:
    # export AZURE_CONTENT_SAFETY_ENDPOINT="https://YOUR_RESOURCE_NAME.cognitiveservices.azure.com/"
    # export AZURE_CONTENT_SAFETY_KEY="YOUR_API_KEY"
    # result = moderate_profile_text("I love everyone! This is a happy profile.")
    # print(result)
    # result_bad = moderate_profile_text("I will kill you. I hate you so much.")
    # print(result_bad)
    pass
