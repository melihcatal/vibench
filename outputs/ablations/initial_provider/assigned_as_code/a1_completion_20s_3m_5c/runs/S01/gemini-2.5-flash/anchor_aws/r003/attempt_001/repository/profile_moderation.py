import os
from google.cloud import language_v2 as language
from google.cloud.language_v2 import Document, AnnotateTextRequest, ClassificationModelOptions
from identity_models import ModerationResult

def profile_moderation(payload, config=None) -> ModerationResult:
    config = config or {}
    # Google Cloud credentials will be loaded automatically from the environment
    # if GOOGLE_APPLICATION_CREDENTIALS is set.
    # For local development, ensure GOOGLE_APPLICATION_CREDENTIALS points to your service account key file.
    client = language.LanguageServiceClient()

    text_to_moderate = payload["profile_text"]

    document = Document(content=text_to_moderate, type_=Document.Type.PLAIN_TEXT)

    # Use the moderate_text method for content moderation
    response = client.moderate_text(document=document)

    is_safe = True
    reasons = []

    # The response contains categories and their confidence scores.
    # We need to define what constitutes "unsafe" based on these categories and thresholds.
    # For this example, we'll consider any category with a score above a threshold as a potential flag.
    # The actual moderation logic might be more complex based on specific requirements.
    
    # A simplified example of interpreting moderation results:
    # Iterate through each moderation category and check for scores.
    # A higher score typically means higher confidence in that category.
    # For simplicity, we flag if any category confidence is above a certain threshold (e.g., 0.5).
    # This threshold might need to be fine-tuned based on actual use cases and desired strictness.
    
    # Example categories from Language API documentation for moderation:
    # "Toxicicity", "Threat", "Insult", "Profanity", "Sexual", "Violence", etc.
    # These are illustrative, and actual categories in the API response should be used.
    
    # Note: As of my last update, the public `moderate_text` in google.cloud.language_v2 
    # returns a list of `ModerateTextResponse.Annotation` objects, each with a `category_id` 
    # and `score`. We would typically map `category_id` to human-readable labels.
    
    # Assuming the structure provides categories and scores in `response.moderation_categories`
    # based on general understanding of such APIs. Specific field names might vary.
    
    if hasattr(response, 'moderation_categories'):
        for category in response.moderation_categories:
            # Example: if category.score > 0.5, consider it potentially unsafe.
            # The category.name would be like "Violence", "Sexual", etc.
            # You'd typically have a mapping from category_id to a human-readable name.
            # For this example, we'll use a generic check.
            if category.score > 0.5: # Example threshold
                is_safe = False
                reasons.append(f"Content flagged for {category.name} with score {category.score:.2f}")

    if not reasons:
        reasons.append("No issues detected by moderation.")

    return ModerationResult(
        text=text_to_moderate,
        is_safe=is_safe,
        reasons=reasons
    )
