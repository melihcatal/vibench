import os
from openai import OpenAI
from security_client import get_openai_client

def check_payload_safety(payload_text: str) -> dict:
    """
    Checks decrypted text payloads for unsafe content using OpenAI's moderation API.
    """
    client = get_openai_client()

    try:
        # OpenAI's moderation API is designed for content safety checks.
        response = client.moderations.create(input=payload_text)
        
        moderation_result = response.results[0]
        
        return {
            "flagged": moderation_result.flagged,
            "categories": moderation_result.categories.model_dump(),
            "category_scores": moderation_result.category_scores.model_dump()
        }
    except Exception as e:
        return {"error": f"Payload safety check failed: {e}"}

if __name__ == '__main__':
    example_safe_payload = "This is a safe and benign message."
    safe_result = check_payload_safety(example_safe_payload)
    print(f"Safe Payload Check Result: {safe_result}")

    # Example of potentially unsafe content (replace with actual unsafe content for testing if desired)
    example_unsafe_payload = "I hate you. I will kill you."
    unsafe_result = check_payload_safety(example_unsafe_payload)
    print(f"Unsafe Payload Check Result: {unsafe_result}")
