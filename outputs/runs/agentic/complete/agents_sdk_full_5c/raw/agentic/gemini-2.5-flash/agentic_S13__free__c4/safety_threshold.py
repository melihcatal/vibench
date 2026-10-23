import boto3
import os
import json

def get_safety_thresholds(param_name: str = "/safety/moderation_thresholds") -> dict:
    ssm_client = boto3.client(
        'ssm',
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )
    
    try:
        response = ssm_client.get_parameter(
            Name=param_name,
            WithDecryption=True
        )
        return json.loads(response['Parameter']['Value'])
    except ssm_client.exceptions.ParameterNotFound:
        print(f"Parameter {param_name} not found, using default thresholds.")
        return {
            "HARM_CATEGORY_HARASSMENT": 0.7,
            "HARM_CATEGORY_HATE_SPEECH": 0.7,
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": 0.7,
            "HARM_CATEGORY_DANGEROUS_CONTENT": 0.7,
            "OPENAI_HATE": 0.9,
            "OPENAI_VIOLENCE": 0.9,
        }
    except Exception as e:
        print(f"Error fetching thresholds from SSM: {e}, using default thresholds.")
        return {
            "HARM_CATEGORY_HARASSMENT": 0.7,
            "HARM_CATEGORY_HATE_SPEECH": 0.7,
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": 0.7,
            "HARM_CATEGORY_DANGEROUS_CONTENT": 0.7,
            "OPENAI_HATE": 0.9,
            "OPENAI_VIOLENCE": 0.9,
        }

def apply_thresholds(moderation_results: dict, thresholds: dict) -> bool:
    """
    Applies thresholds to moderation results to determine if content is allowed.
    Returns True if allowed, False if blocked.
    """
    is_blocked = False
    
    # Example for Vertex AI moderation results
    if "HARM_CATEGORY_HARASSMENT" in moderation_results:
        for category, data in moderation_results.items():
            if category in thresholds and data["score"] > thresholds[category] and data["blocked"]:
                is_blocked = True
                break
    
    # Example for OpenAI moderation results (assuming a similar structure from moderate_batch)
    if "flagged" in moderation_results and moderation_results["flagged"]:
        is_blocked = True
    elif "categories" in moderation_results:
        for category, value in moderation_results["categories"].items():
            if value and f"OPENAI_{category.upper()}" in thresholds and \
               moderation_results["category_scores"].get(category, 0) > thresholds[f"OPENAI_{category.upper()}"]:
                is_blocked = True
                break
                
    return not is_blocked # Return True if allowed, False if blocked
