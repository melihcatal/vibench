import os
from typing import List, Dict, Any
from messaging_client import AWSMessagingClient
from messaging_models import ContentSafetyRequest, ContentSafetyResult


def check_message_safety(request: ContentSafetyRequest) -> ContentSafetyResult:
    """Checks message payload text for unsafe content using Amazon Comprehend (DetectToxicContent)."""
    comprehend_client = AWSMessagingClient().get_comprehend_client()

    try:
        response = comprehend_client.detect_toxic_content(
            Text=request.text,
            LanguageCode="en",  # Assuming English for this example, can be dynamic
        )

        toxic_content_list = response.get("Result", {}).get("Toxicity", [])

        is_unsafe = False
        moderation_labels: List[Dict[str, Any]] = []

        if toxic_content_list:
            for toxic_category in toxic_content_list:
                category = toxic_category.get("Name")
                score = toxic_category.get("Score")
                # Define a threshold for what is considered "unsafe"
                # This threshold might need tuning based on specific requirements
                if score > 0.7:  # Example threshold
                    is_unsafe = True
                moderation_labels.append(
                    {
                        "category": category,
                        "score": score,
                        "is_high_score": score
                        > 0.7,  # Indicates if it crossed the example threshold
                    }
                )

        return ContentSafetyResult(
            is_unsafe=is_unsafe, moderation_labels=moderation_labels
        )
    except Exception as e:
        print(f"Error checking content safety with Comprehend: {e}")
        return ContentSafetyResult(
            is_unsafe=True,
            moderation_labels=[{"category": "error", "score": 1.0, "detail": str(e)}],
        )


if __name__ == "__main__":
    # Example Usage
    safe_text = "Hello, how are you today? This is a perfectly safe message."
    unsafe_text = (
        "I hate you! You are the worst person ever. I'm going to do something bad."
    )

    safety_request_safe = ContentSafetyRequest(text=safe_text)
    safety_result_safe = check_message_safety(safety_request_safe)
    print("\n--- Safe Message Check ---")
    print(f'Text: "{safe_text}"')
    print(f"Is Unsafe: {safety_result_safe.is_unsafe}")
    print(f"Moderation Labels: {safety_result_safe.moderation_labels}")

    safety_request_unsafe = ContentSafetyRequest(text=unsafe_text)
    safety_result_unsafe = check_message_safety(safety_request_unsafe)
    print("\n--- Unsafe Message Check ---")
    print(f'Text: "{unsafe_text}"')
    print(f"Is Unsafe: {safety_result_unsafe.is_unsafe}")
    print(f"Moderation Labels: {safety_result_unsafe.moderation_labels}")
