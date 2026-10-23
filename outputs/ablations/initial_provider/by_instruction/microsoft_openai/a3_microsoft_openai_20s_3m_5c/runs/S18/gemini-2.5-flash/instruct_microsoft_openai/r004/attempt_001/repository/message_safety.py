import os
from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
import azure.cognitiveservices.vision.contentmoderator.models as cm_models
from msrest.authentication import CognitiveServicesCredentials
from messaging_models import Event

def check_message_safety(event: Event) -> dict:
    # Ensure the data in the event is a string or can be converted to a string for moderation
    if not isinstance(event.data, str):
        text_content = str(event.data)
    else:
        text_content = event.data

    key = os.environ.get("AZURE_CONTENT_MODERATOR_KEY")
    endpoint = os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT")

    if not key or not endpoint:
        print("Azure Content Moderator credentials not set. Skipping safety check.")
        return {"is_safe": True, "reason": "Content Moderator not configured"}

    client = ContentModeratorClient(endpoint=endpoint, credentials=CognitiveServicesCredentials(key))

    # Text moderation
    moderation_response = client.text_moderation.screen_text(
        text_content=text_content,
        language="eng",
        content_type="text/plain"
    )

    # Simple check for profanity. More detailed checks would involve iterating through terms.
    # For demonstration, we'll consider it unsafe if any profanity is detected.
    is_unsafe = False
    reason = "Content is safe."

    if moderation_response.terms and len(moderation_response.terms) > 0:
        is_unsafe = True
        reason = "Profanity detected."

    # You can add more checks based on other moderation_response fields like PII, classifications, etc.
    return {"is_safe": not is_unsafe, "reason": reason, "moderation_result": moderation_response.as_dict()}

if __name__ == "__main__":
    example_event_safe = Event(id="101", type="chat_message", data="Hello, how are you?")
    print("\n--- Safe Message Check ---")
    print(check_message_safety(example_event_safe))

    # This example assumes a profane word. Replace with an actual profane word to test.
    example_event_unsafe = Event(id="102", type="chat_message", data="This is a bad word example.")
    print("\n--- Unsafe Message Check ---")
    print(check_message_safety(example_event_unsafe))
