import os
from google.cloud import language_v1

def check_unsafe_content(text_content):
    """
    Checks message payload text for unsafe content using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Available categories: https://cloud.google.com/natural-language/docs/reference/rest/v1/ModerateTextResponse#ModerationCategory
    response = client.moderate_text(document=document)
    
    # You can process the response to determine if content is unsafe based on your criteria.
    # For example, checking the score of each category.
    # This example simply returns the full response.
    return response

if __name__ == "__main__":
    # Example usage
    text_to_check = "I want to harm myself."
    # Make sure to set GOOGLE_APPLICATION_CREDENTIALS environment variable
    # or authenticate otherwise for Google Cloud client libraries.
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    
    # Check if the environment variable is set
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable.")
        print("For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"")
    else:
        print(f"Checking text: \"{text_to_check}\"")
        result = check_unsafe_content(text_to_check)
        print("Moderation Result:")
        for category_score in result.moderation_categories:
            print(f"  Category: {category_score.name}, Score: {category_score.score:.2f}")

    text_to_check_2 = "Hello, how are you today?"
    if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        print(f"\nChecking text: \"{text_to_check_2}\"")
        result_2 = check_unsafe_content(text_to_check_2)
        print("Moderation Result:")
        for category_score in result_2.moderation_categories:
            print(f"  Category: {category_score.name}, Score: {category_score.score:.2f}")
