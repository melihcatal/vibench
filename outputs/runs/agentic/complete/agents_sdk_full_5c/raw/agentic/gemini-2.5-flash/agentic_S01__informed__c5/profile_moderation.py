import os
import requests
import json

def profile_moderation(text: str) -> dict:
    # Azure AI Content Safety configuration
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set in environment variables.")

    # The API version for Content Safety
    api_version = "2023-10-01"
    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "outputType": "FourSeverityLevels"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()
        return {"moderation_results": result}
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to moderate text with Azure AI Content Safety: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during moderation: {e}")

if __n__ == '__main__':
    # Example usage (requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY to be set)
    # import os
    # os.environ['AZURE_CONTENT_SAFETY_ENDPOINT'] = "https://YOUR_RESOURCE_NAME.cognitiveservices.azure.com/"
    # os.environ['AZURE_CONTENT_SAFETY_KEY'] = "YOUR_CONTENT_SAFETY_KEY"
    # try:
    #     profile_text = "This is a normal profile. I like puppies."
    #     moderation_output = profile_moderation(profile_text)
    #     print(f"Moderation for '{profile_text}': {moderation_output}")
    #
    #     toxic_text = "I hate everyone and want to hurt them."
    #     toxic_moderation_output = profile_moderation(toxic_text)
    #     print(f"Moderation for '{toxic_text}': {toxic_moderation_output}")
    #
    # except RuntimeError as e:
    #     print(f"Error during moderation: {e}")
    # except ValueError as e:
    #     print(f"Configuration error: {e}")
    pass
