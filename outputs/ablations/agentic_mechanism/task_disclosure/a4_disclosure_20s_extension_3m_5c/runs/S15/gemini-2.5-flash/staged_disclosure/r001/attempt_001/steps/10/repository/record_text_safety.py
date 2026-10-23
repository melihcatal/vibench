import os
from google.cloud import language_v2

def check_text_safety(text_content: str):
    """
    Checks user-generated text for unsafe content using Google Cloud Natural Language API.
    """
    client = language_v2.LanguageServiceClient()

    document = language_v2.Document(
        content=text_content, type_=language_v2.Document.Type.PLAIN_TEXT
    )

    # Use the moderate_text feature to check for unsafe content
    response = client.moderate_text(document=document)

    # You can process the response to identify unsafe categories
    # For example, to print categories and their scores:
    # for category in response.moderation_categories:
    #     print(f"Category: {category.name}, Score: {category.score}")

    return response

if __name__ == "__main__":
    # Example usage:
    text_to_check = "I hate you. You are a terrible person."
    print(f"Checking text: \"{text_to_check}\"")
    safety_result = check_text_safety(text_to_check)

    if safety_result.moderation_categories:
        print("Moderation Categories:")
        for category in safety_result.moderation_categories:
            print(f"  Category: {category.name}, Score: {category.score:.2f}")
    else:
        print("No moderation categories found (text might be safe or no specific issues detected).")

    text_to_check_2 = "This is a wonderful day filled with joy and happiness!"
    print(f"\nChecking text: \"{text_to_check_2}\"")
    safety_result_2 = check_text_safety(text_to_check_2)

    if safety_result_2.moderation_categories:
        print("Moderation Categories:")
        for category in safety_result_2.moderation_categories:
            print(f"  Category: {category.name}, Score: {category.score:.2f}")
    else:
        print("No moderation categories found (text might be safe or no specific issues detected).")
