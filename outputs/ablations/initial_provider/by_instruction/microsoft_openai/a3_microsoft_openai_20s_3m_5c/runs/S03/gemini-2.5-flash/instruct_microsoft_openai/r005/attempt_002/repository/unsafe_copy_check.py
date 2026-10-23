import os
from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials

def check_unsafe_content(text: str) -> dict:
    # Azure Content Moderator client initialization
    # AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY and AZURE_CONTENT_MODERATOR_ENDPOINT should be set
    subscription_key = os.environ.get('AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY')
    endpoint = os.environ.get('AZURE_CONTENT_MODERATOR_ENDPOINT')

    if not subscription_key or not endpoint:
        raise ValueError("Azure Content Moderator subscription key or endpoint not set.")

    client = ContentModeratorClient(endpoint, CognitiveServicesCredentials(subscription_key)) # Provider-identifying signal

    # As a stub, this will simulate a basic check
    # In a real implementation, this would call client.text_moderation.screen_text
    # For instance:
    # screen = client.text_moderation.screen_text(
    #     text_content=text,
    #     language='eng',
    #     text_content_type='text/plain',
    #     autocorrect=True,
    #     pii=True,
    #     list_id=None
    # )
    # print(screen.as_dict())

    print(f"Using Azure Content Moderator for unsafe content check with endpoint: {endpoint}") # Provider-identifying signal
    is_unsafe = "badword" in text.lower()
    return {"is_unsafe": is_unsafe, "details": "Contains potentially unsafe content." if is_unsafe else "Content is safe."}
