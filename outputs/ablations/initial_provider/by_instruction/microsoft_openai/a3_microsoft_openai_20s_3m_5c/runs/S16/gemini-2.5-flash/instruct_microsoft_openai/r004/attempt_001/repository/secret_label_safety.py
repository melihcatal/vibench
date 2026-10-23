from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials
import os

def check_secret_label_safety(text: str) -> dict:
    """
    Checks secret labels and notes for unsafe text using Azure Content Moderator.
    """
    subscription_key = os.environ.get("AZURE_CONTENT_MODERATOR_KEY")
    endpoint = os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT")

    if not subscription_key or not endpoint:
        raise ValueError("AZURE_CONTENT_MODERATOR_KEY and AZURE_CONTENT_MODERATOR_ENDPOINT environment variables must be set.")

    client = ContentModeratorClient(endpoint=endpoint, credentials=CognitiveServicesCredentials(subscription_key))

    try:
        # Check for profanity
        text_screen = client.text_moderation.screen_text(text_content=text, language="eng", detect_profanity=True)
        
        # Check for PII (Personal Identifiable Information) - usually done with custom lists or classification
        # For simplicity, this example focuses on profanity and general text review.
        # More advanced checks would involve custom term lists or a broader classification.

        is_safe = True
        unsafe_categories = []

        if text_screen.terms:
            is_safe = False
            unsafe_categories.append("Profanity")

        # You can add more checks here, e.g., for custom blocked terms lists
        # term_list_id = os.environ.get("AZURE_CONTENT_MODERATOR_TERMLIST_ID")
        # if term_list_id:
        #     custom_screen = client.text_moderation.screen_text(
        #         text_content=text, language="eng", list_id=term_list_id
        #     )
        #     if custom_screen.terms:
        #         is_safe = False
        #         unsafe_categories.append("Custom_Blocked_Terms")

        return {
            "is_safe": is_safe,
            "unsafe_categories": unsafe_categories,
            "raw_moderation_result": text_screen.as_dict() # Return full result for detailed analysis
        }
    except Exception as e:
        raise RuntimeError(f"Failed to check secret label safety with Azure Content Moderator: {e}")

if __name__ == '__main__':
    # Example usage (requires AZURE_CONTENT_MODERATOR_KEY and AZURE_CONTENT_MODERATOR_ENDPOINT)
    # Set environment variables before running
    # print(check_secret_label_safety("This is a test label with some bad words."))
    # print(check_secret_label_safety("This is a safe label."))
    pass
