
import os
from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
import azure.cognitiveservices.vision.contentmoderator.models as contentmoderator_models
from msrest.authentication import CognitiveServicesCredentials

def moderate_text_claim(text_claim: str) -> dict:
    # Azure Content Moderator client setup
    SUBSCRIPTION_KEY = os.environ.get("AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY")
    ENDPOINT = os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT")

    if not SUBSCRIPTION_KEY or not ENDPOINT:
        raise ValueError("Azure Content Moderator subscription key and endpoint must be set in environment variables.")

    client = ContentModeratorClient(
        endpoint=ENDPOINT,
        credentials=CognitiveServicesCredentials(SUBSCRIPTION_KEY)
    )

    print(f"Moderating text: '{text_claim}'")
    
    # Moderate the text for profanity, sentiment, etc.
    text_screen = client.text_moderation.screen_text(
        text_content=text_claim,
        language="eng", # Assuming English for now, can be made dynamic
        autocorrect=True,
        pii=True, # Personal Identifiable Information
        classify=True # Multi-label text classification
    )

    # Extract relevant moderation results
    moderation_results = {
        "original_text": text_claim,
        "profanity": text_screen.profanity.is_profane if text_screen.profanity else False,
        "terms": [],
        "classification": {
            "category1": text_screen.classification.category1.score if text_screen.classification and text_screen.classification.category1 else None,
            "category2": text_screen.classification.category2.score if text_screen.classification and text_screen.classification.category2 else None,
            "category3": text_screen.classification.category3.score if text_screen.classification and text_screen.classification.category3 else None,
            "review_recommended": text_screen.classification.review_recommended if text_screen.classification else False
        },
        "pii_found": text_screen.pii.email if text_screen.pii else None # More detailed PII handling would be here
    }

    if text_screen.terms:
        for term in text_screen.terms:
            moderation_results["terms"].append({"term": term.term, "index": term.index})

    print(f"Moderation Results: {moderation_results}")
    return moderation_results

if __name__ == '__main__':
    # Example usage: Set your Azure Content Moderator credentials
    # os.environ['AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY'] = 'YOUR_SUBSCRIPTION_KEY'
    # os.environ['AZURE_CONTENT_MODERATOR_ENDPOINT'] = 'YOUR_ENDPOINT'

    test_claim_clean = "This is a perfectly fine comment about my profile."
    test_claim_profane = "This claim contains some **badword** content!"
    test_claim_pii = "My email is test@example.com and phone is 555-123-4567."

    # Ensure environment variables are set before running
    if os.environ.get("AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY") and os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT"):
        print("\n--- Moderating Clean Claim ---")
        moderate_text_claim(test_claim_clean)

        print("\n--- Moderating Profane Claim ---")
        moderate_text_claim(test_claim_profane)

        print("\n--- Moderating PII Claim ---")
        moderate_text_claim(test_claim_pii)
    else:
        print("Please set AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY and AZURE_CONTENT_MODERATOR_ENDPOINT environment variables to run this example.")

