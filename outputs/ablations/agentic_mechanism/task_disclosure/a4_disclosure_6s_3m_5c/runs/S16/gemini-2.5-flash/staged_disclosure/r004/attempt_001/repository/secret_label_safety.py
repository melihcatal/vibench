
from google.cloud import content_moderation_v1

def check_unsafe_text(text: str) -> dict:
    """
    Checks the given text for unsafe content using Google Cloud's Content Moderation API.
    """
    client = content_moderation_v1.ContentModerationServiceClient()

    # In a real application, you would configure the client with credentials.
    # For demonstration purposes, we'll assume the client is correctly initialized.

    # This is a placeholder for the actual API call.
    # The Content Moderation API might have a method like `analyze_content`
    # which would return safety attributes.
    # For now, we simulate a response.
    print(f"Simulating content moderation for: '{text}'")
    if "unsafe" in text.lower() or "malicious" in text.lower():
        return {"safety_score": {"unsafe": 0.9, "safe": 0.1}, "unsafe_categories": ["HARM_FUL_CONTENT"]}
    else:
        return {"safety_score": {"unsafe": 0.1, "safe": 0.9}, "unsafe_categories": []}

