import os
from google.cloud import language_v2

def check_safety(text_payload: str) -> dict:
    """
    Checks the given text payload for unsafe content using Google Cloud's Language AI.

    Args:
        text_payload: The decrypted text content to check.

    Returns:
        A dictionary containing the moderation results.
    """
    # Instantiates a client
    client = language_v2.LanguageServiceClient()

    # The document to analyze
    document = language_v2.Document(
        content=text_payload, 
        type_=language_v2.Document.Type.PLAIN_TEXT
    )

    # Detects safety attributes of the text
    response = client.moderate_text(document=document)

    # Process the results
    # The response object will contain a list of categories with their scores.
    # A score closer to 1 indicates a higher likelihood of the content belonging to that category.
    safety_results = {}
    for category in response.moderation_categories:
        safety_results[category.name] = category.score
            
    return safety_results

if __name__ == '''__main__''':
    # Example Usage:
    # Ensure you have authenticated to Google Cloud. 
    # For local development, you can use `gcloud auth application-default login`
    
    # Example 1: Safe content
    safe_text = "Hello, this is a perfectly safe and friendly message."
    print(f"Safety check for safe text: {check_safety(safe_text)}")

    # Example 2: Potentially unsafe content (replace with your actual test case)
    # Note: The actual scores will depend on Google's moderation model.
    unsafe_text = "This text contains some potentially inappropriate language like insults."
    print(f"Safety check for potentially unsafe text: {check_safety(unsafe_text)}")
