import json
from typing import List

# Hosted Content Moderation example: Alibaba Cloud Content Moderation
# Uses the alibabacloud_green SDK for unsafe content detection


def check_unsafe(localized_copy: List[str]) -> List[bool]:
    """Detect unsafe content in localized copy using Alibaba Cloud Content Moderation.

    Args:
        localized_copy: List of translated text strings to assess.

    Returns:
        List of booleans indicating safety (True = safe, False = unsafe) for each entry.
    """
    # Import the moderation client inside to isolate dependency
    from alibabacloud_green20200514.client import Client
    from alibabacloud_tea_openapi.models import Config

    # Ensure ALIBABA credentials are present
    ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    if not ACCESS_KEY_ID or not ACCESS_KEY_SECRET:
        raise RuntimeError(
            "ALIBABA_CLOUD_ACCESS_KEY_ID or ALIBABA_CLOUD_ACCESS_KEY_SECRET not set"
        )

    # Configure the green client
    config = Config(
        accessKeyId=ACCESS_KEY_ID,
        accessKeySecret=ACCESS_KEY_SECRET,
        endpoint="green.cn-hangzhou.aliyuncs.com",
    )
    client = Client(config)

    # Alibaba Content Moderation API request payload per text
    def is_safe(text: str) -> bool:
        response = client.text_mod(
            {
                "scenes": ["ads"],  # primary unsafe category; extend as needed
                "content": text,
            }
        )
        # Parse JSON response
        result = response.get("resp", {}).get("results", [])
        # Simple heuristic: if any category is flagged as unsafe, mark as unsafe
        for item in result:
            if item.get("label") == "ads":
                return False
        return True

    # Batch evaluation (one request per string for simplicity)
    results = [is_safe(text) for text in localized_copy]
    return results


# Example usage when run directly (requires Alibaba credentials)
if __name__ == "__main__":
    examples = [
        "Hello, world!",
        "Buy cheap watches here!",  # may be flagged as ads
    ]
    safety_flags = check_unsafe(examples)
    for txt, safe in zip(examples, safety_flags):
        print(f"Text: {txt} => Safe: {safe}")
