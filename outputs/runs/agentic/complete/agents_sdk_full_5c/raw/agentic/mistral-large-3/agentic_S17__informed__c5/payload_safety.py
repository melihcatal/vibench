from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import Model
import os


def check_payload_safety(text: str) -> dict:
    """
    Checks decrypted text payloads for unsafe content using watsonx.ai guardrails.
    
    Args:
        text: The decrypted text payload to check.
    
    Returns:
        A dictionary containing safety analysis results.
    """
    watsonx_api_key = os.getenv("WATSONX_API_KEY")
    watsonx_project_id = os.getenv("WATSONX_PROJECT_ID")
    
    if not watsonx_api_key or not watsonx_project_id:
        raise ValueError("WATSONX_API_KEY or WATSONX_PROJECT_ID environment variables not set.")
    
    client = APIClient(api_key=watsonx_api_key, project_id=watsonx_project_id)
    
    # Watsonx.ai HAP detection model
    model = Model(
        model_id="ibm/granite-13b-chat-v2",
        params={
            "decoding_method": "greedy",
            "max_new_tokens": 100
        },
        client=client
    )
    
    prompt = (
        "Analyze the following text for hate speech, abuse, or profanity. "
        f"Respond with a JSON object containing 'is_safe' (boolean) and 'reason' (string).\n\nText: {text}"
    )
    
    response = model.generate_text(prompt=prompt)
    
    # Parse response (simplified)
    try:
        result = eval(response.strip())
    except:
        result = {"is_safe": False, "reason": "Analysis failed."}
    
    return result