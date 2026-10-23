import os
import requests
from model_models import ModerationRequest, ModerationResponse


def check_prompt_safety(text: str) -> ModerationResponse:
    """
    Checks prompts and generated text for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}

    request_body = {"text": text}

    try:
        response = requests.post(url, headers=headers, json=request_body)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        result = response.json()

        # Parse the result into ModerationResponse model
        categories_analysis = result.get("categoriesAnalysis", [])
        harm_blockages = result.get("harmBlockages", [])

        return ModerationResponse(
            categories_analysis=categories_analysis, harm_blockages=harm_blockages
        )
    except requests.exceptions.RequestException as e:
        print(f"Error checking content safety: {e}")
        # Return a default/empty response in case of error
        return ModerationResponse(categories_analysis=[], harm_blockages=[])


if __name__ == "__main__":
    # Example usage:
    # os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"] = "YOUR_AZURE_CONTENT_SAFETY_ENDPOINT"
    # os.environ["AZURE_CONTENT_SAFETY_KEY"] = "YOUR_AZURE_CONTENT_SAFETY_KEY"

    # safe_text = "Hello, how are you today?"
    # unsafe_text = "I hate you!"

    # print(f"Safety check for safe text: {check_prompt_safety(safe_text)}")
    # print(f"Safety check for unsafe text: {check_prompt_safety(unsafe_text)}")
    pass
