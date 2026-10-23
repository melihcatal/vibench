import os
from google.cloud import language_v2 # Provider-specific SDK import
from google.api_core.exceptions import GoogleAPIError

def check_unsafe_text(text_content: str) -> dict:
    """
    Checks the given text content for unsafe or policy-sensitive text using Google Cloud Natural Language API.

    Args:
        text_content: The text string to be analyzed for safety.

    Returns:
        A dictionary containing the moderation results.
    """
    try:
        client = language_v2.LanguageServiceClient()
        document = language_v2.Document(content=text_content, type_=language_v2.Document.Type.PLAIN_TEXT)
        
        # Google Cloud Natural Language API endpoint for content moderation is implicitly handled by the client
        # model_id can be specified for some operations, but for content moderation, it's typically managed by the service.

        response = client.moderate_text(document=document)
        
        moderation_feedback = {}
        for category_filter in response.moderation_categories:
            moderation_feedback[category_filter.name] = category_filter.score

        return {"moderation_results": moderation_feedback}

    except GoogleAPIError as e:
        # Handle Google Cloud API errors
        return {"error": f"Google Cloud API Error: {e.message}"}
    except Exception as e:
        # Handle other potential errors
        return {"error": f"An unexpected error occurred: {str(e)}"}

if __name__ == '__main__':
    # Example usage (ensure GOOGLE_APPLICATION_CREDENTIALS is set up for local testing)
    # For local testing, ensure you have authenticated with `gcloud auth application-default login`
    # or set the GOOGLE_APPLICATION_CREDENTIALS environment variable.

    test_text_safe = "This is a beautiful image of a landscape with trees and a river."
    test_text_unsafe = "This image contains hate speech and violence."

    print(f"Checking safe text: '{test_text_safe}'")
    result_safe = check_unsafe_text(test_text_safe)
    print(result_safe)

    print(f"Checking unsafe text: '{test_text_unsafe}'")
    result_unsafe = check_unsafe_text(test_text_unsafe)
    print(result_unsafe)
