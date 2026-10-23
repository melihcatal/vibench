from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials
import os

def check_unsafe_content(text: str) -> dict:
    # Azure Content Moderator credentials
    subscription_key = os.getenv("AZURE_MODERATOR_KEY")
    endpoint = os.getenv("AZURE_MODERATOR_ENDPOINT")

    if not subscription_key or not endpoint:
        return {"error": "Azure Content Moderator key or endpoint not found."}

    client = ContentModeratorClient(
        endpoint=endpoint,
        credentials=CognitiveServicesCredentials(subscription_key)
    )

    # Screen the text for profanity, classification, and personal data
    try:
        screen = client.text_moderation.screen_text(text_content=text, language='eng', classify=True)
        
        # Extracting relevant information from the screen object
        classification = screen.classify if screen.classify else None
        contains_profanity = bool(screen.terms) if screen.terms else False
        
        # Prepare a more readable output
        result = {
            "original_text": text,
            "language": 'eng', # Language used for moderation
            "profanity_detected": contains_profanity,
            "classification": {
                "category1_score": classification.category1.score if classification and classification.category1 else 0.0,
                "category2_score": classification.category2.score if classification and classification.category2 else 0.0,
                "category3_score": classification.category3.score if classification and classification.category3 else 0.0,
                "review_recommended": classification.review_recommended if classification else False
            },
            "terms": [{'term': term.term, 'index': term.index} for term in screen.terms] if screen.terms else []
        }

        return result
    except Exception as e:
        return {"error": f"Content Moderator API error: {str(e)}"}
