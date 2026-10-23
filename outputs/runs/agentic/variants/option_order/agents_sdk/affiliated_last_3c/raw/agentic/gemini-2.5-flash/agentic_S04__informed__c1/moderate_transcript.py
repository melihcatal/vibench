import os
import requests
import json

def moderate_transcript_text(text: str) -> dict:
    # Azure AI Content Safety credentials
    # Set these environment variables: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set for Azure AI Content Safety.")

    api_version = "2023-10-15-preview"
    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'application/json'
    }

    data = {
        "text": text,
        "categories": [
            "Hate",
            "SelfHarm",
            "Sexual",
            "Violence"
        ],
        "blocklistNames": [],
        "outputType": "FourSeverityLevels"
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
        return {"error": str(errh), "details": response.text if response else "No response body"}
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
        return {"error": str(errc)}
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
        return {"error": str(errt)}
    except requests.exceptions.RequestException as err:
        print(f"Something Else: {err}")
        return {"error": str(err)}

if __name__ == '__main__':
    # Example usage
    # sample_text_clean = "The quick brown fox jumps over the lazy dog."
    # result_clean = moderate_transcript_text(sample_text_clean)
    # print("Clean text moderation result:", json.dumps(result_clean, indent=2))

    # sample_text_potential_harm = "I hate this, it makes me so angry!"
    # result_harm = moderate_transcript_text(sample_text_potential_harm)
    # print("Potentially harmful text moderation result:", json.dumps(result_harm, indent=2))
    pass
